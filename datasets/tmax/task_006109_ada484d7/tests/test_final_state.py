# test_final_state.py

import os
import json
import pytest

def test_summary_json_exists():
    """Check that the summary.json file was created in the correct location."""
    file_path = "/home/user/summary.json"
    assert os.path.isfile(file_path), f"File not found: {file_path}. The script did not generate the output file."

def test_summary_json_contents():
    """Check that the summary.json file contains the correct aggregated statistics."""
    file_path = "/home/user/summary.json"
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    expected_data = {
        "sensor_A": 0.4,
        "sensor_B": 0.4071,
        "sensor_C": 0.0
    }

    assert isinstance(data, dict), f"Expected JSON root to be a dictionary, got {type(data).__name__}."

    # Check keys
    assert set(data.keys()) == set(expected_data.keys()), f"Expected keys {set(expected_data.keys())}, but got {set(data.keys())}."

    # Check values with a small tolerance for floating point issues, though it should be exactly rounded to 4 decimal places
    for key, expected_value in expected_data.items():
        actual_value = data[key]
        assert isinstance(actual_value, (int, float)), f"Value for {key} should be a number, got {type(actual_value).__name__}."
        assert round(actual_value, 4) == expected_value, f"Value for {key} is incorrect. Expected {expected_value}, got {actual_value}."