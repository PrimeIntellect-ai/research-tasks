# test_final_state.py

import os
import pytest
import math

def test_c_source_exists():
    path = "/home/user/solve_and_compare.c"
    assert os.path.exists(path), f"Missing C source file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

def test_kl_result_exists_and_correct():
    result_path = "/home/user/kl_result.txt"
    expected_path = "/tmp/expected_kl.txt"

    assert os.path.exists(result_path), f"Missing result file: {result_path}"
    assert os.path.isfile(result_path), f"Not a file: {result_path}"

    assert os.path.exists(expected_path), f"Missing expected file: {expected_path}"

    with open(result_path, 'r') as f:
        actual_str = f.read().strip()

    with open(expected_path, 'r') as f:
        expected_str = f.read().strip()

    try:
        actual = float(actual_str)
    except ValueError:
        pytest.fail(f"Result in {result_path} is not a valid float: '{actual_str}'")

    try:
        expected = float(expected_str)
    except ValueError:
        pytest.fail(f"Expected value in {expected_path} is not a valid float: '{expected_str}'")

    tolerance = 1e-10
    diff = abs(actual - expected)
    assert diff < tolerance, f"Actual KL divergence ({actual}) differs from expected ({expected}) by {diff}, which is >= {tolerance}"