apt-get update && apt-get install -y python3 python3-pip curl gcc make build-essential cargo rustc
    pip3 install pytest

    mkdir -p /home/user/workspace/math_lib_c
    mkdir -p /home/user/workspace/rust_app/src

    cat << 'EOF' > /home/user/workspace/math_lib_c/matrix_math.h
#ifndef MATRIX_MATH_H
#define MATRIX_MATH_H

const char* get_version();
int* multiply_matrices(const int* a, const int* b, int size);
void free_matrix(int* matrix);

#endif
EOF

    cat << 'EOF' > /home/user/workspace/math_lib_c/matrix_math.c
#include "matrix_math.h"
#include <stdlib.h>

const char* get_version() {
    return "1.3.5";
}

int* multiply_matrices(const int* a, const int* b, int size) {
    // BUG: size * sizeof(int) instead of size * size * sizeof(int)
    int* result = (int*)malloc(size * sizeof(int));
    if (!result) return NULL;

    for(int i = 0; i < size; i++) {
        for(int j = 0; j < size; j++) {
            int sum = 0;
            for(int k = 0; k < size; k++) {
                sum += a[i * size + k] * b[k * size + j];
            }
            result[i * size + j] = sum;
        }
    }
    return result;
}

void free_matrix(int* matrix) {
    if (matrix) free(matrix);
}
EOF

    cat << 'EOF' > /home/user/workspace/math_lib_c/Makefile
all:
	gcc -o libmatrixmath.so matrix_math.c
EOF

    cat << 'EOF' > /home/user/workspace/rust_app/Cargo.toml
[package]
name = "rust_app"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

    cat << 'EOF' > /home/user/workspace/rust_app/src/main.rs
fn main() {
    println!("Hello, world!");
}
EOF

    cat << 'EOF' > /home/user/workspace/verifier.py
def verify_trace(matrix, size):
    trace = 0
    for i in range(size):
        trace += matrix[i * size + i]
    return trace

# Note: The output matrix C = A * B.
# For the specific 5x5 matrices in the prompt, 
# trace will be evaluated mathematically to 3315.
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user