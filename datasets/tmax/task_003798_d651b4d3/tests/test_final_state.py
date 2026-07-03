# test_final_state.py

import os
import ctypes
import re

BASE_DIR = "/home/user/math_service"

def test_libfastmath_so_exists_and_valid():
    lib_path = os.path.join(BASE_DIR, "libfastmath.so")
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist."

    try:
        lib = ctypes.CDLL(lib_path)
    except Exception as e:
        pytest.fail(f"Failed to load {lib_path} as a shared library: {e}")

    assert hasattr(lib, "fast_inv_sqrt"), "Library is missing the fast_inv_sqrt function."

def test_math_ops_fixed():
    py_file = os.path.join(BASE_DIR, "math_ops.py")
    assert os.path.isfile(py_file), f"File {py_file} does not exist."
    with open(py_file, "r") as f:
        content = f.read()

    assert "c_double" not in content, "math_ops.py still contains c_double."
    assert "c_float" in content, "math_ops.py does not use ctypes.c_float."

def test_api_fixed():
    api_file = os.path.join(BASE_DIR, "api.py")
    assert os.path.isfile(api_file), f"File {api_file} does not exist."
    with open(api_file, "r") as f:
        content = f.read()

    has_float_route = "<float:value>" in content
    has_float_cast = "float(value)" in content or "float(" in content
    assert has_float_route or has_float_cast, "api.py does not cast the parameter to float or use <float:value> in the route."

def test_test_api_fixed():
    test_file = os.path.join(BASE_DIR, "test_api.py")
    assert os.path.isfile(test_file), f"File {test_file} does not exist."
    with open(test_file, "r") as f:
        content = f.read()

    assert "hypothesis" in content, "test_api.py does not import hypothesis."
    assert "test_inv_sqrt_property" in content, "test_api.py is missing the test_inv_sqrt_property function."
    assert "0.1" in content and "1000.0" in content, "test_api.py does not seem to use the 0.1 to 1000.0 range for the property test."

def test_test_results_log():
    log_file = os.path.join(BASE_DIR, "test_results.log")
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."
    with open(log_file, "r") as f:
        content = f.read()

    assert "passed" in content.lower() or "ok" in content.lower(), "test_results.log does not indicate that the tests passed."
    assert "failed" not in content.lower() or "0 failed" in content.lower(), "test_results.log indicates that tests failed."