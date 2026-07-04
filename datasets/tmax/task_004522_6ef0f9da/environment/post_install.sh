apt-get update && apt-get install -y python3 python3-pip python3-dev build-essential
    pip3 install pytest

    mkdir -p /home/user/telemetry_project

    cat << 'EOF' > /home/user/telemetry_project/setup.py
from setuptools import setup, Extension

# BUG: Missing math library linkage which causes undefined reference to 'pow' and 'sqrt'
fastparse_module = Extension('fastparse',
                             sources=['fastparse.c'],
                             libraries=[]) # Should be ['m']

setup(name='fastparse',
      version='1.0',
      description='Fast telemetry parser',
      ext_modules=[fastparse_module])
EOF

    cat << 'EOF' > /home/user/telemetry_project/fastparse.c
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <math.h>

static PyObject* parse_record(PyObject* self, PyObject* args) {
    const char* data;
    Py_ssize_t data_len;

    if (!PyArg_ParseTuple(args, "y#", &data, &data_len)) {
        return NULL;
    }

    if (data_len < 2) {
        PyErr_SetString(PyExc_ValueError, "Data too short");
        return NULL;
    }

    int type = data[0];
    int payload_len = data[1];

    // BUG: Missing bounds check for payload_len. 

    char buffer[16];
    // This will segfault if payload_len is larger than 16
    for(int i = 0; i < payload_len; i++) {
        buffer[i] = data[2 + i];
    }

    // Dummy math operation to force libm dependency
    double dummy = sqrt(pow((double)type, 2.0));

    return Py_BuildValue("id", type, dummy);
}

static PyMethodDef FastParseMethods[] = {
    {"parse_record",  parse_record, METH_VARARGS, "Parse a record."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fastparsemodule = {
    PyModuleDef_HEAD_INIT,
    "fastparse",
    NULL,
    -1,
    FastParseMethods
};

PyMODINIT_FUNC PyInit_fastparse(void) {
    return PyModuleCreate(&fastparsemodule);
}
EOF

    cat << 'EOF' > /home/user/telemetry_project/main.py
import fastparse
import struct

def calculate_metric(velocity, wind_speed, drag_coefficient):
    # BUG: Formula implementation error
    # FIX: return (velocity + wind_speed) * drag_coefficient / 2.0
    return velocity + wind_speed * drag_coefficient / 2.0

def main():
    records = [
        b'\x01\x04ABCD', # Valid
        b'\x02\x04EFGH', # Valid
        b'\x03\xff' + b'X'*255, # Malformed edge-case causing segfault
        b'\x04\x02YZ'    # Valid
    ]

    results = []
    for r in records:
        try:
            parsed = fastparse.parse_record(r)
            # Mock data extraction
            velocity = 100.0
            wind_speed = 10.0
            drag_coefficient = 0.5

            metric = calculate_metric(velocity, wind_speed, drag_coefficient)
            results.append(f"Type: {parsed[0]}, Metric: {metric}")
        except ValueError as e:
            results.append(f"Error: {e}")

    with open("results.txt", "w") as f:
        for res in results:
            f.write(res + "\n")

if __name__ == "__main__":
    main()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user