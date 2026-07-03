# test_final_state.py

import os
import re
import pytest

WORKSPACE_DIR = "/home/user/workspace"
MATH_LIB_C_DIR = os.path.join(WORKSPACE_DIR, "math_lib_c")
RUST_APP_DIR = os.path.join(WORKSPACE_DIR, "rust_app")
RESULT_FILE = os.path.join(WORKSPACE_DIR, "result.txt")
SO_FILE = os.path.join(MATH_LIB_C_DIR, "libmatrixmath.so")
C_FILE = os.path.join(MATH_LIB_C_DIR, "matrix_math.c")
BUILD_RS = os.path.join(RUST_APP_DIR, "build.rs")

def test_c_library_built():
    assert os.path.isfile(SO_FILE), f"Shared object not found: {SO_FILE}"

    with open(SO_FILE, "rb") as f:
        header = f.read(4)
        assert header == b"\x7fELF", f"{SO_FILE} is not a valid ELF file"

def test_c_code_fixed():
    assert os.path.isfile(C_FILE), f"C file missing: {C_FILE}"

    with open(C_FILE, "r") as f:
        content = f.read()
        # The bug was `size * sizeof(int)`. It should be fixed to allocate size*size elements.
        # Check if it multiplies size * size (or size*size)
        assert re.search(r"size\s*\*\s*size", content) is not None, \
            "The memory allocation bug in matrix_math.c does not appear to be fixed (missing size * size)."

def test_rust_build_rs_exists():
    assert os.path.isfile(BUILD_RS), f"build.rs not found: {BUILD_RS}"
    with open(BUILD_RS, "r") as f:
        content = f.read()
        assert "matrixmath" in content or "math_lib_c" in content, \
            "build.rs does not seem to configure the linking for the C library."

def test_result_file():
    assert os.path.isfile(RESULT_FILE), f"Result file missing: {RESULT_FILE}"

    with open(RESULT_FILE, "r") as f:
        content = f.read().strip()

    assert content == "3315", f"Result file contains '{content}', expected '3315'."