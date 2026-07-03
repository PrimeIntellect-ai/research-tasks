# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_test_results_log_exists_and_passed():
    log_path = os.path.join(PROJECT_DIR, "test_results.log")
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did the tests run successfully?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "PASSED" in content, f"Expected 'PASSED' in {log_path}, but got: {content}"

def test_shared_library_built_correctly():
    lib_path = os.path.join(PROJECT_DIR, "libmathops.so")
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist."

    # Check if it's a shared object
    file_output = subprocess.check_output(["file", lib_path], text=True)
    assert "shared object" in file_output, f"{lib_path} is not a shared object. Output: {file_output}"

    # Check if it links against math library
    ldd_output = subprocess.check_output(["ldd", lib_path], text=True)
    assert "libm.so" in ldd_output, f"{lib_path} does not link against libm.so. Did you forget -lm?"

def test_makefile_fixed():
    makefile_path = os.path.join(PROJECT_DIR, "Makefile")
    assert os.path.isfile(makefile_path), f"Makefile {makefile_path} does not exist."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-shared" in content, "Makefile is missing the '-shared' flag."
    assert "-fPIC" in content, "Makefile is missing the '-fPIC' flag."
    assert "-lm" in content, "Makefile is missing the '-lm' flag to link the math library."

def test_python_script_fixed():
    py_path = os.path.join(PROJECT_DIR, "test_mathops.py")
    assert os.path.isfile(py_path), f"Python script {py_path} does not exist."

    with open(py_path, "r") as f:
        content = f.read()

    assert "argtypes" in content, "test_mathops.py is missing 'argtypes' definition for the C function."
    assert "restype" in content, "test_mathops.py is missing 'restype' definition for the C function."
    assert "c_double" in content, "test_mathops.py is missing ctypes.c_double in argtypes."
    assert "c_int" in content, "test_mathops.py is missing ctypes.c_int in restype."