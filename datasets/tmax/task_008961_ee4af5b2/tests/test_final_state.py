# test_final_state.py

import os
import json
import pytest

RESULT_FILE = '/home/user/ci_results.json'

def test_result_file_exists():
    """Test that the expected JSON output file exists."""
    assert os.path.isfile(RESULT_FILE), f"Expected result file not found at {RESULT_FILE}"

def test_result_file_format_and_values():
    """Test that the JSON file contains the correct keys and values within expected ranges."""
    with open(RESULT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULT_FILE} is not a valid JSON file.")

    expected_keys = {"mean", "lower_bound", "upper_bound"}
    actual_keys = set(data.keys())
    assert expected_keys.issubset(actual_keys), f"JSON is missing expected keys. Found: {actual_keys}, Expected: {expected_keys}"

    for key in expected_keys:
        assert isinstance(data[key], (int, float)), f"Value for '{key}' must be a number, got {type(data[key])}"

    mean = data["mean"]
    lower = data["lower_bound"]
    upper = data["upper_bound"]

    # Check against expected approximate ranges based on N=10000 bootstrap iterations
    assert 0.32 <= mean <= 0.36, f"Mean value {mean} is outside the expected range [0.32, 0.36]."
    assert 0.24 <= lower <= 0.29, f"Lower bound value {lower} is outside the expected range [0.24, 0.29]."
    assert 0.40 <= upper <= 0.44, f"Upper bound value {upper} is outside the expected range [0.40, 0.44]."