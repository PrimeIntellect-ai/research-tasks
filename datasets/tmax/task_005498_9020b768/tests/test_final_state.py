# test_final_state.py

import os
import pytest

def test_fit_result_exists_and_correct():
    result_file = "/home/user/fit_result.txt"

    # Check if the file exists
    assert os.path.exists(result_file), f"Fail: {result_file} not found. Did you run the script after fixing it?"
    assert os.path.isfile(result_file), f"Fail: {result_file} is not a regular file."

    # Read the content
    with open(result_file, "r") as f:
        content = f.read().strip()

    # Check if it's a valid float
    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Fail: The content of {result_file} ('{content}') is not a valid float.")

    # Check if the value is within the expected bounds
    assert 3.5300 <= val <= 3.5450, f"Fail: Value {val} is out of the expected bounds [3.5300, 3.5450]. The Monte Carlo integration might still be incorrect."