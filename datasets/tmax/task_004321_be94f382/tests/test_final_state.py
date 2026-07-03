# test_final_state.py

import os
import json
import pytest

def test_regression_result_exists():
    """Test that the regression_result.json file was created."""
    file_path = "/home/user/regression_result.json"
    assert os.path.isfile(file_path), f"Expected file {file_path} was not found."

def test_regression_result_content():
    """Test that the regression_result.json file contains the correct model parameters."""
    file_path = "/home/user/regression_result.json"
    assert os.path.isfile(file_path), f"Expected file {file_path} was not found."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    assert "slope" in data, "JSON is missing the 'slope' key."
    assert "intercept" in data, "JSON is missing the 'intercept' key."

    # Check values with a small tolerance for floating point representation of 4 decimal places
    expected_slope = 1.8000
    expected_intercept = 3.3333

    slope = data["slope"]
    intercept = data["intercept"]

    assert isinstance(slope, (int, float)), f"'slope' must be a number, got {type(slope)}"
    assert isinstance(intercept, (int, float)), f"'intercept' must be a number, got {type(intercept)}"

    assert round(slope, 4) == expected_slope, f"Expected slope to be {expected_slope}, but got {slope}"
    assert round(intercept, 4) == expected_intercept, f"Expected intercept to be {expected_intercept}, but got {intercept}"