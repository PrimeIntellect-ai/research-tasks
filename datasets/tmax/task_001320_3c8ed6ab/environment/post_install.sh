apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest numpy

    mkdir -p /app/libmatrix-0.1.0/src

    cat << 'EOF' > /app/libmatrix-0.1.0/src/matrix_ops.h
#ifndef MATRIX_OPS_H
#define MATRIX_OPS_H

typedef struct {
    int rows;
    int cols;
    double *data;
} Matrix;

Matrix* create_matrix(int rows, int cols);
void free_matrix(Matrix *m);
Matrix* multiply_matrices(Matrix *A, Matrix *B);

#endif
EOF

    cat << 'EOF' > /app/libmatrix-0.1.0/src/matrix_ops.c
#include <stdlib.h>
#include "matrix_ops.h"

Matrix* create_matrix(int rows, int cols) {
    Matrix *m = (Matrix*)malloc(sizeof(Matrix));
    m->rows = rows;
    m->cols = cols;
    m->data = (double*)calloc(rows * cols, sizeof(double));
    return m;
}

void free_matrix(Matrix *m) {
    if (m) {
        free(m->data);
        free(m);
    }
}

Matrix* multiply_matrices(Matrix *A, Matrix *B) {
    if (A->cols != B->rows) return NULL;
    Matrix *C = create_matrix(A->rows, B->cols);

    // Bug: i <= A->rows (off-by-one)
    for (int i = 0; i <= A->rows; i++) {
        for (int j = 0; j < B->cols; j++) {
            for (int k = 0; k < A->cols; k++) {
                C->data[i * C->cols + j] += A->data[i * A->cols + k] * B->data[k * B->cols + j];
            }
        }
    }
    return C;
}
EOF

    cat << 'EOF' > /app/libmatrix-0.1.0/Makefile
CC = gcc
CFLAGS = -O3 -Wall

all: libmatrix.so

matrix_ops.o: src/matrix_ops.c
	$(CC) $(CFLAGS) -c src/matrix_ops.c -o matrix_ops.o

libmatrix.so: matrix_ops.o
	$(CC) -o libmatrix.so matrix_ops.o

clean:
	rm -f *.o *.so
EOF

    cat << 'EOF' > /app/libmatrix-0.1.0/ffi_caller.py
import sys
import ctypes
import os

class Matrix(ctypes.Structure):
    _fields_ = [
        ("rows", ctypes.c_int),
        ("cols", ctypes.c_int),
        ("data", ctypes.POINTER(ctypes.c_double))
    ]

def load_matrix(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        rows = len(lines)
        cols = len(lines[0].strip().split())
        m_ptr = lib.create_matrix(rows, cols)
        for i, line in enumerate(lines):
            vals = list(map(float, line.strip().split()))
            for j, val in enumerate(vals):
                m_ptr.contents.data[i * cols + j] = val
        return m_ptr

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)

    lib_path = os.path.join(os.path.dirname(__file__), "libmatrix.so")
    try:
        lib = ctypes.CDLL(lib_path)
    except OSError as e:
        print("Failed to load library")
        sys.exit(1)

    lib.create_matrix.restype = ctypes.POINTER(Matrix)
    lib.multiply_matrices.restype = ctypes.POINTER(Matrix)

    m1 = load_matrix(sys.argv[1])
    m2 = load_matrix(sys.argv[2])

    res = lib.multiply_matrices(m1, m2)

    if res:
        for i in range(res.contents.rows):
            row_vals = []
            for j in range(res.contents.cols):
                row_vals.append(str(res.contents.data[i * res.contents.cols + j]))
            print(" ".join(row_vals))

    lib.free_matrix(m1)
    lib.free_matrix(m2)
    lib.free_matrix(res)
EOF

    chmod -R 777 /app/libmatrix-0.1.0

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user