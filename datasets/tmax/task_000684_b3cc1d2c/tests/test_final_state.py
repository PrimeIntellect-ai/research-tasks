# test_final_state.py

import os
import sys
import subprocess
import ctypes
import pytest

def compute_truth(n):
    """Derive the expected recurrence relation value natively in Python."""
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, (3 * b + 2 * a) % 998244353
    return b

def test_build_and_test_exists_and_executable():
    path = "/home/user/math_project/build_and_test.sh"
    assert os.path.isfile(path), f"{path} is missing. Did you create the bash script?"
    assert os.access(path, os.X_OK), f"{path} is not executable. Check file permissions."

def test_pipeline_execution():
    script_path = "/home/user/math_project/build_and_test.sh"

    # Run from a different directory to ensure paths are handled correctly in the wrapper and script
    result = subprocess.run(["bash", script_path], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"build_and_test.sh failed with return code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    log_path = "/home/user/pipeline_result.log"
    assert os.path.isfile(log_path), f"{log_path} was not created by the pipeline script."

    with open(log_path, "r") as f:
        log_content = f.read()

    expected_val = compute_truth(1000)
    expected_str = f"PIPELINE_OK: SEQ_1000={expected_val}"
    assert expected_str in log_content, f"Expected '{expected_str}' in {log_path}, got: {log_content}"

def test_math_wrapper_ffi():
    # Ensure the shared library exists before trying to import
    so_path = "/home/user/math_project/libfastmath.so"
    assert os.path.isfile(so_path), f"{so_path} is missing. Compilation step may have failed."

    sys.path.insert(0, "/home/user/math_project")
    try:
        import math_wrapper
        func = math_wrapper.lib.compute_seq

        assert hasattr(func, "argtypes") and func.argtypes is not None, "argtypes not set on compute_seq in math_wrapper.py"
        assert hasattr(func, "restype") and func.restype is not None, "restype not set on compute_seq in math_wrapper.py"

        assert func.argtypes == [ctypes.c_uint32], f"argtypes should be [ctypes.c_uint32], got {func.argtypes}"
        assert func.restype == ctypes.c_uint64, f"restype should be ctypes.c_uint64, got {func.restype}"

        # Test the function itself to verify the wrapper logic
        expected_1000 = compute_truth(1000)
        actual_1000 = math_wrapper.get_seq(1000)
        assert actual_1000 == expected_1000, f"get_seq(1000) returned incorrect value. Expected {expected_1000}, got {actual_1000}"
    finally:
        sys.path.pop(0)