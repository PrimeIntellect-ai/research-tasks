apt-get update && apt-get install -y python3 python3-pip python3-dev build-essential openssl
    pip3 install pytest cryptography setuptools

    mkdir -p /app/custom_b64-1.0

    # Generate dummy certificate
    openssl req -x509 -newkey rsa:2048 -keyout /tmp/key.pem -out /app/server.crt -days 365 -nodes -subj "/CN=localhost"

    # Create custom_b64.c
    cat << 'EOF' > /app/custom_b64-1.0/custom_b64.c
#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject* custom_b64_decode(PyObject* self, PyObject* args) {
    const char* input;
    Py_ssize_t length;
    if (!PyArg_ParseTuple(args, "s#", &input, &length)) {
        return NULL;
    }
    PyObject* base64_mod = PyImport_ImportModule("base64");
    if (!base64_mod) return NULL;
    PyObject* decode_func = PyObject_GetAttrString(base64_mod, "b64decode");
    if (!decode_func) { Py_DECREF(base64_mod); return NULL; }
    PyObject* res = PyObject_CallFunction(decode_func, "s#", input, length);
    Py_DECREF(decode_func);
    Py_DECREF(base64_mod);
    if (!res) {
        PyErr_SetString(PyExc_ValueError, "Decode failed");
        return NULL;
    }
    return res;
}

static PyMethodDef CustomB64Methods[] = {
    {"decode", custom_b64_decode, METH_VARARGS, "Decode custom base64"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef customb64module = {
    PyModuleDef_HEAD_INIT,
    "custom_b64",
    NULL,
    -1,
    CustomB64Methods
};

PyMODINIT_FUNC PyInit_custom_b64(void) {
    return PyModule_Create(&customb64module);
}
EOF

    # Create setup.py with perturbation
    cat << 'EOF' > /app/custom_b64-1.0/setup.py
from setuptools import setup, Extension

setup(
    name='custom_b64',
    version='1.0',
    ext_modules=[Extension('custom_b64', sources=['wrong_source.c'])]
)
EOF

    # Create oracle checker
    cat << 'EOF' > /app/oracle_checker
#!/usr/bin/env python3
import sys
import base64
import hashlib
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def main():
    data = sys.stdin.read()
    auth_val = None
    for line in data.split('\n'):
        if line.lower().startswith('x-secure-auth:'):
            auth_val = line.split(':', 1)[1].strip()
            break

    if not auth_val:
        print("DENY:MISSING_HEADER")
        return

    try:
        decoded = base64.b64decode(auth_val).decode('utf-8')
    except Exception:
        print("ERROR:DECODE_FAIL")
        return

    parts = decoded.split('|')
    if len(parts) != 3:
        print("ERROR:DECODE_FAIL")
        return

    username, role, cert_sha256_hex = parts

    try:
        with open('/app/server.crt', 'rb') as f:
            cert_data = f.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            actual_fp = cert.fingerprint(hashes.SHA256()).hex()
    except Exception:
        actual_fp = ""

    if cert_sha256_hex != actual_fp:
        print("DENY:CERT_MISMATCH")
        return

    if role == 'admin':
        print("GRANT:ADMIN")
    else:
        print("GRANT:USER")

if __name__ == '__main__':
    main()
EOF
    chmod +x /app/oracle_checker

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user