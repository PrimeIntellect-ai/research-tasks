# test_final_state.py

import os
import json
import pytest

def test_drift_metrics_file_exists():
    path = "/home/user/drift_metrics.json"
    assert os.path.isfile(path), f"Missing output file: {path}"

def test_drift_metrics_format_and_values():
    path = "/home/user/drift_metrics.json"
    assert os.path.isfile(path), f"Missing output file: {path}"

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not a valid JSON.")

    required_keys = {"distance", "ci_lower", "ci_upper"}
    missing_keys = required_keys - set(data.keys())
    assert not missing_keys, f"Missing keys in JSON output: {missing_keys}"

    # Check if they are floats
    for key in required_keys:
        assert isinstance(data[key], (int, float)), f"Value for '{key}' must be a number."

    # The expected values are deterministic based on the provided setup and seed
    expected_distance = 0.2081
    expected_ci_lower = 0.0531
    expected_ci_upper = 0.3541

    assert abs(data["distance"] - expected_distance) < 1e-4, \
        f"Expected distance around {expected_distance}, got {data['distance']}"

    assert abs(data["ci_lower"] - expected_ci_lower) < 1e-4, \
        f"Expected ci_lower around {expected_ci_lower}, got {data['ci_lower']}"

    assert abs(data["ci_upper"] - expected_ci_upper) < 1e-4, \
        f"Expected ci_upper around {expected_ci_upper}, got {data['ci_upper']}"