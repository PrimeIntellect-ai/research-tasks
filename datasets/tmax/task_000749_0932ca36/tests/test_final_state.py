# test_final_state.py

import os
import json
import math
import pytest

def test_regression_results_exists():
    file_path = "/home/user/regression_results.json"
    assert os.path.isfile(file_path), f"Expected output file {file_path} is missing. Did the Go program run and generate it?"

def test_regression_results_content():
    file_path = "/home/user/regression_results.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    # Check for required keys
    required_keys = {"valid_count", "slope", "intercept", "slope_std_error"}
    missing_keys = required_keys - set(data.keys())
    assert not missing_keys, f"JSON output is missing required keys: {missing_keys}"

    # Validate valid_count
    assert data["valid_count"] == 6, f"Expected valid_count to be 6, but got {data['valid_count']}. Make sure you are dropping rows that fail to parse as standard 64-bit floats."

    # Validate slope
    expected_slope = 193.6496699669967
    assert math.isclose(data["slope"], expected_slope, rel_tol=1e-3), \
        f"Expected slope to be close to {expected_slope}, but got {data['slope']}."

    # Validate intercept
    expected_intercept = 12831.68316831671
    assert math.isclose(data["intercept"], expected_intercept, rel_tol=1e-3), \
        f"Expected intercept to be close to {expected_intercept}, but got {data['intercept']}."

    # Validate slope_std_error
    expected_std_error = 11.167374
    assert math.isclose(data["slope_std_error"], expected_std_error, rel_tol=1e-3), \
        f"Expected slope_std_error to be close to {expected_std_error}, but got {data['slope_std_error']}."