# test_final_state.py

import os
import pytest

def test_result_accuracy():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Expected result file missing: {result_path}"

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content, f"Result file {result_path} is empty"

    try:
        result_val = float(content)
    except ValueError:
        pytest.fail(f"Result file {result_path} does not contain a valid float: {content}")

    expected = 0.5
    error = abs(result_val - expected)
    tolerance = 1e-7

    assert error <= tolerance, f"Numerical error {error} exceeds tolerance {tolerance}. Result was {result_val}, expected ~{expected}."