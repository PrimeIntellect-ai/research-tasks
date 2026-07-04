# test_final_state.py

import os
import re
import pytest

def test_source_code_exists():
    """Check that the C++ source code file exists."""
    assert os.path.isfile("/home/user/diffusion.cpp"), "Source code file /home/user/diffusion.cpp is missing."

def test_executable_exists():
    """Check that the compiled executable exists."""
    assert os.path.isfile("/home/user/diffusion"), "Executable /home/user/diffusion is missing."
    assert os.access("/home/user/diffusion", os.X_OK), "/home/user/diffusion is not executable."

def test_results_log_exists():
    """Check that the results.log file exists."""
    assert os.path.isfile("/home/user/results.log"), "Results file /home/user/results.log is missing."

def test_results_log_content():
    """Check that the results.log file contains the correct values."""
    log_path = "/home/user/results.log"
    assert os.path.isfile(log_path), f"{log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    # Parse key-value pairs
    results = {}
    for line in content.strip().split("\n"):
        if "=" in line:
            key, val = line.split("=", 1)
            try:
                results[key.strip()] = float(val.strip())
            except ValueError:
                pytest.fail(f"Could not parse value for {key}: {val}")

    expected = {
        "M": 10000.00,
        "mu_x": 404.50,
        "mu_y": 604.50,
        "var_x": 208.25,
        "var_y": 208.25,
        "cov_xy": 0.00
    }

    for key, expected_val in expected.items():
        assert key in results, f"Missing key {key} in results.log"
        actual_val = results[key]
        assert abs(actual_val - expected_val) <= 0.05, f"Value for {key} is {actual_val}, expected ~{expected_val}"