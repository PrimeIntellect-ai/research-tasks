apt-get update && apt-get install -y python3 python3-pip python3-dev build-essential ffmpeg valgrind

pip3 install pytest hypothesis

mkdir -p /home/user/project/src
mkdir -p /home/user/project/include
mkdir -p /app

cat << 'EOF' > /home/user/project/setup.py
from setuptools import setup, Extension

module1 = Extension('fast_processor',
                    sources = ['src/processor.c'],
                    include_dirs = ['include'])

setup (name = 'FastProcessor',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])
EOF

cat << 'EOF' > /home/user/project/src/processor.c
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "helper.h"

static PyObject* process_string(PyObject* self, PyObject* args) {
    const char* input;
    if (!PyArg_ParseTuple(args, "s", &input)) {
        return NULL;
    }

    // Vulnerability: no length check, fixed buffer
    char buffer[100];
    strcpy(buffer, input);

    char output[100];
    process_logic(buffer, output);

    return Py_BuildValue("s", output);
}

static PyMethodDef FastProcessorMethods[] = {
    {"process_string",  process_string, METH_VARARGS, "Process a string."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fastprocessormodule = {
    PyModuleDef_HEAD_INIT,
    "fast_processor",
    NULL,
    -1,
    FastProcessorMethods
};

PyMODINIT_FUNC PyInit_fast_processor(void) {
    return PyModule_Create(&fastprocessormodule);
}
EOF

cat << 'EOF' > /home/user/project/src/helper.c
#include "helper.h"
#include <string.h>

void process_logic(const char* input, char* output) {
    int len = strlen(input);
    for(int i=0; i<len; i++) {
        char c = input[len - 1 - i];
        if (c >= 'a' && c <= 'z') {
            output[i] = ((c - 'a' + 13) % 26) + 'a';
        } else if (c >= 'A' && c <= 'Z') {
            output[i] = ((c - 'A' + 13) % 26) + 'A';
        } else {
            output[i] = c;
        }
    }
    output[len] = '\0';
}
EOF

cat << 'EOF' > /home/user/project/include/helper.h
#ifndef HELPER_H
#define HELPER_H
void process_logic(const char* input, char* output);
#endif
EOF

cat << 'EOF' > /app/oracle_processor.py
import sys
def process(s):
    s = s[:37]
    import codecs
    return codecs.encode(s[::-1], 'rot_13')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(process(sys.argv[1]), end="")
    else:
        print("", end="")
EOF

# Generate glitch.mp4 with exactly 37 red frames
ffmpeg -y -f lavfi -i color=c=red:s=32x32:r=10 -frames:v 37 /tmp/red.mp4
ffmpeg -y -f lavfi -i color=c=blue:s=32x32:r=10 -frames:v 13 /tmp/blue.mp4
echo "file '/tmp/red.mp4'" > /tmp/list.txt
echo "file '/tmp/blue.mp4'" >> /tmp/list.txt
ffmpeg -y -f concat -safe 0 -i /tmp/list.txt -c copy /app/glitch.mp4
rm /tmp/red.mp4 /tmp/blue.mp4 /tmp/list.txt

useradd -m -s /bin/bash user || true
chown -R user:user /home/user
chmod -R 777 /home/user
chmod -R 777 /app