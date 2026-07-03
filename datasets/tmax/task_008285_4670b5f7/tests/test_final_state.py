# test_final_state.py

import json
import os
import math

def test_json_file_exists():
    """Check if the distribution_metrics.json file was created."""
    path = '/home/user/distribution_metrics.json'
    assert os.path.exists(path), f"File missing: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

def test_json_contents():
    """Check if the JSON file contains the correct keys and values."""
    path = '/home/user/distribution_metrics.json'

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "The file distribution_metrics.json is not valid JSON."

    expected_keys = {"mean_ll", "ci_lower", "ci_upper"}
    actual_keys = set(data.keys())
    assert actual_keys == expected_keys, f"JSON keys do not match. Expected {expected_keys}, found {actual_keys}"

    # Expected values derived from the fixed random seeds in setup and task
    expected_values = {
        "mean_ll": -3.8344,
        "ci_lower": -3.9452,
        "ci_upper": -3.7292
    }

    for key in expected_keys:
        val = data[key]
        assert isinstance(val, (int, float)), f"Value for '{key}' is not a number."
        assert math.isclose(val, expected_values[key], abs_tol=1e-4), \
            f"Value for '{key}' is incorrect. Expected approximately {expected_values[key]}, got {val}"