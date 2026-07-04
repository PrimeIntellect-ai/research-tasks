# test_final_state.py
import os
import json
import pytest

def test_bootstrap_results():
    file_path = "/home/user/bootstrap_results.json"
    assert os.path.isfile(file_path), f"Missing required file: {file_path}"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    assert "lower_bound" in data, f"Missing 'lower_bound' key in {file_path}"
    assert "upper_bound" in data, f"Missing 'upper_bound' key in {file_path}"

    lower = data["lower_bound"]
    upper = data["upper_bound"]

    assert isinstance(lower, (int, float)), f"'lower_bound' must be a number, got {type(lower)}"
    assert isinstance(upper, (int, float)), f"'upper_bound' must be a number, got {type(upper)}"

    # Check bounds against expected values with a tolerance of 0.1
    expected_lower = 49.03
    expected_upper = 50.18

    assert abs(lower - expected_lower) <= 0.1, f"'lower_bound' {lower} is not within 0.1 of expected {expected_lower}"
    assert abs(upper - expected_upper) <= 0.1, f"'upper_bound' {upper} is not within 0.1 of expected {expected_upper}"

def test_bvp_result():
    file_path = "/home/user/bvp_result.txt"
    assert os.path.isfile(file_path), f"Missing required file: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "4.5000", f"Expected content of {file_path} to be '4.5000', got '{content}'"