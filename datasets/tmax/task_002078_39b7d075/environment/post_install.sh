apt-get update && apt-get install -y python3 python3-pip python3-dev gcc make binutils
    pip3 install pytest numpy setuptools

    mkdir -p /home/user/project
    mkdir -p /app

    # Create fast_math.c (with bug)
    cat << 'EOF' > /home/user/project/fast_math.c
#include <Python.h>
#include <math.h>

static PyObject* compute(PyObject* self, PyObject* args) {
    double x;
    if (!PyArg_ParseTuple(args, "d", &x)) {
        return NULL;
    }
    double sum = 0.0;
    for (int k = 1; k <= 50; k++) {
        if (k > 25) {
            sum += sin(k * x) / k; // BUG
        } else {
            sum += sin(k * x) / (k * k);
        }
    }
    return PyFloat_FromDouble(sum);
}

static PyMethodDef FastMathMethods[] = {
    {"compute", compute, METH_VARARGS, "Compute the series."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fastmathmodule = {
    PyModuleDef_HEAD_INIT,
    "fast_math",
    NULL,
    -1,
    FastMathMethods
};

PyMODINIT_FUNC PyInit_fast_math(void) {
    return PyModule_Create(&fastmathmodule);
}
EOF

    # Create setup.py (missing libraries=['m'])
    cat << 'EOF' > /home/user/project/setup.py
from setuptools import setup, Extension
module = Extension('fast_math', sources=['fast_math.c'])
setup(name='fast_math', ext_modules=[module])
EOF

    # Create oracle C source
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    double x = atof(argv[1]);
    double sum = 0.0;
    for (int k = 1; k <= 50; k++) {
        sum += sin(k * x) / (k * k);
    }
    printf("%.15f\n", sum);
    return 0;
}
EOF

    # Compile and strip oracle
    gcc -O3 /tmp/oracle.c -o /app/math_oracle -lm
    strip /app/math_oracle

    # Generate inputs.csv and reference_outputs.txt
    cat << 'EOF' > /tmp/generate_data.py
import numpy as np

np.random.seed(42)
inputs = np.random.uniform(-10.0, 10.0, 10000)

with open('/home/user/project/inputs.csv', 'w') as f_in, open('/tmp/reference_outputs.txt', 'w') as f_out:
    for val in inputs:
        f_in.write(f"{val}\n")
        sum_val = sum(np.sin(k * val) / (k * k) for k in range(1, 51))
        f_out.write(f"{sum_val}\n")
EOF
    python3 /tmp/generate_data.py

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user