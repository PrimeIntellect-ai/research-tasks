# test_final_state.py

import os
import json
import math
import pytest

def test_venv_exists():
    venv_path = "/home/user/venv"
    assert os.path.isdir(venv_path), f"Virtual environment directory not found at {venv_path}"

    # Check for bin/python to ensure it's a valid venv
    python_path = os.path.join(venv_path, "bin", "python")
    assert os.path.isfile(python_path), f"Python executable not found in virtual environment at {python_path}"

def test_analysis_results_json():
    json_path = "/home/user/analysis_results.json"
    assert os.path.isfile(json_path), f"Results JSON file not found at {json_path}"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected_keys = {"correlation", "t_statistic", "p_value"}
    actual_keys = set(data.keys())
    assert actual_keys == expected_keys, f"JSON keys mismatch. Expected {expected_keys}, got {actual_keys}"

    expected_values = {
        "correlation": 0.8493,
        "t_statistic": 22.0125,
        "p_value": 0.0
    }

    for key, expected_val in expected_values.items():
        actual_val = data[key]
        assert isinstance(actual_val, (int, float)), f"Value for '{key}' must be a number, got {type(actual_val)}"
        assert math.isclose(actual_val, expected_val, abs_tol=1e-4), \
            f"Value for '{key}' is incorrect. Expected ~{expected_val}, got {actual_val}"