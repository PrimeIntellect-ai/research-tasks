# test_final_state.py
import os
import json
import pytest

def test_results_json_exists():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Output file not found at: {results_path}"

def test_results_json_content():
    results_path = "/home/user/results.json"
    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} does not contain valid JSON.")

    expected_keys = {"correlation", "ci_lower", "ci_upper"}
    assert set(data.keys()) == expected_keys, f"JSON keys do not match expected. Found: {list(data.keys())}"

    expected_values = {
        "correlation": 0.0409,
        "ci_lower": -0.3421,
        "ci_upper": 0.4137
    }

    tolerance = 0.0002

    for key, expected_val in expected_values.items():
        actual_val = data[key]
        assert isinstance(actual_val, (int, float)), f"Value for '{key}' must be a number."
        assert abs(actual_val - expected_val) <= tolerance, \
            f"Value for '{key}' is {actual_val}, expected {expected_val} (tolerance {tolerance})"