# test_final_state.py

import os
import numpy as np
import pytest

def test_result_file_exists():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"Missing result file at {path}"

def test_libmathops_so_exists():
    path = "/home/user/math_module/libmathops.so"
    assert os.path.isfile(path), f"Missing shared library at {path}. Did the Makefile run successfully?"

def test_ffi_test_py_exists():
    path = "/home/user/math_module/ffi_test.py"
    assert os.path.isfile(path), f"Missing Python FFI script at {path}"

def test_result_mse():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"Result file {path} not found."

    try:
        with open(path, "r") as f:
            agent_out = np.array([float(line.strip()) for line in f.readlines()])
    except Exception as e:
        pytest.fail(f"Failed to read and parse {path}: {e}")

    assert len(agent_out) == 100000, f"Expected 100,000 lines in {path}, got {len(agent_out)}"

    x = np.linspace(0.0, 10.0, 100000, dtype=np.float32)
    expected = 2.5 * (x**3) - 1.2 * (x**2) + 0.5 * x - 3.1
    mse = np.mean((agent_out - expected)**2)

    threshold = 0.001
    assert mse <= threshold, f"MSE {mse} exceeds threshold {threshold}. The polynomial calculation is incorrect."