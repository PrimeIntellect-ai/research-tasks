# test_final_state.py

import os
import json
import math
import pytest

def test_metrics_json_exists_and_valid():
    """Check if metrics.json is created and contains the correct keys."""
    file_path = "/home/user/metrics.json"
    assert os.path.isfile(file_path), f"Output file is missing: {file_path}"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    expected_keys = {"threshold", "filtered_mean", "ci_lower", "ci_upper"}
    assert set(data.keys()) == expected_keys, f"JSON keys do not match. Expected {expected_keys}, got {set(data.keys())}"

def test_metrics_values():
    """Check if the values in metrics.json match the expected ground truth within 0.0001 tolerance."""
    file_path = "/home/user/metrics.json"
    assert os.path.isfile(file_path), f"Output file is missing: {file_path}"

    with open(file_path, "r") as f:
        data = json.load(f)

    expected_metrics = {
        "threshold": 4.1481,
        "filtered_mean": 0.7027,
        "ci_lower": 0.5843,
        "ci_upper": 0.8170
    }

    for key, expected_val in expected_metrics.items():
        actual_val = data.get(key)
        assert actual_val is not None, f"Missing key '{key}' in metrics.json"
        assert isinstance(actual_val, (int, float)), f"Value for '{key}' must be a number"
        assert math.isclose(actual_val, expected_val, abs_tol=0.0002), (
            f"Value for '{key}' is incorrect. Expected ~{expected_val}, got {actual_val}"
        )