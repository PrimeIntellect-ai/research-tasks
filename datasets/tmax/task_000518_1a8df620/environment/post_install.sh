apt-get update && apt-get install -y python3 python3-pip python3-dev build-essential ffmpeg
    pip3 install pytest setuptools wheel

    mkdir -p /home/user/ocr_extractor/ocr_extractor

    cat << 'EOF' > /home/user/ocr_extractor/setup.py
from setuptools import setup, Extension

ext = Extension(
    'ocr_extractor._ext',
    sources=['ocr_extractor/_ext.c'],
    include_dirs=['/usr/include/nonexistent'],
    # libraries=['m'] intentionally omitted
)

setup(
    name='ocr_extractor',
    version='0.1',
    packages=['ocr_extractor'],
    ext_modules=[ext],
)
EOF

    cat << 'EOF' > /home/user/ocr_extractor/ocr_extractor/__init__.py
from ._ext import do_math
EOF

    cat << 'EOF' > /home/user/ocr_extractor/ocr_extractor/__main__.py
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m ocr_extractor <image_path>")
        sys.exit(1)
    img_path = sys.argv[1]

    # Mock OCR behavior
    if "0188" in img_path or "0187" in img_path:
        print("goroutine leak triggered at 0xc00008e000")
    else:
        print("no text found")

if __name__ == "__main__":
    main()
EOF

    cat << 'EOF' > /home/user/ocr_extractor/ocr_extractor/_ext.c
#include <Python.h>
#include <math.h>

static PyObject* do_math(PyObject* self, PyObject* args) {
    double x;
    if (!PyArg_ParseTuple(args, "d", &x)) return NULL;
    return PyFloat_FromDouble(pow(x, 2.0));
}

static PyMethodDef methods[] = {
    {"do_math", do_math, METH_VARARGS, "Do math"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "_ext", NULL, -1, methods
};

PyMODINIT_FUNC PyInit__ext(void) {
    return PyModule_Create(&module);
}
EOF

    mkdir -p /app/training_data/evil /app/training_data/clean
    mkdir -p /app/corpus/evil /app/corpus/clean

    cat << 'EOF' > /app/training_data/evil/log1.txt
context canceled
goroutine 123 [chan receive]
EOF

    cat << 'EOF' > /app/training_data/clean/log1.txt
context canceled
sync.WaitGroup done
EOF

    cat << 'EOF' > /app/corpus/evil/log1.txt
context canceled
goroutine 999 [chan receive]
EOF

    cat << 'EOF' > /app/corpus/clean/log1.txt
context canceled
normal exit
EOF

    # Generate a dummy video with 300 frames
    ffmpeg -f lavfi -i color=c=black:s=320x240:r=30 -frames:v 300 -c:v libx264 -preset ultrafast /app/suspicious_execution.mp4

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user
    chmod -R 777 /app