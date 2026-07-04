# test_final_state.py

import os
import json
import pytest

def test_result_json_exists_and_valid():
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"The result file is missing at {result_path}"

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {result_path} does not contain valid JSON.")

    # Check required keys
    required_keys = {"k_max", "s_max", "best_alpha", "min_error"}
    missing_keys = required_keys - set(data.keys())
    assert not missing_keys, f"Missing required keys in result.json: {missing_keys}"

    # Verify k_max
    assert data["k_max"] == 500000, f"Expected k_max=500000, got {data.get('k_max')}"

    # Verify best_alpha bounds
    best_alpha = data["best_alpha"]
    assert isinstance(best_alpha, (int, float)), "best_alpha must be a number"
    assert 4.0 < best_alpha < 5.5, f"best_alpha {best_alpha} is out of expected bounds (4.0, 5.5)"

    # Verify s_max and min_error types
    assert isinstance(data["s_max"], (int, float)), "s_max must be a number"
    assert isinstance(data["min_error"], (int, float)), "min_error must be a number"