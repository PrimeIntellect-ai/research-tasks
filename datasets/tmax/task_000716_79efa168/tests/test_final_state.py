# test_final_state.py
import json
import os
import pytest
import math

def test_solution_json_exists_and_valid():
    """Test that solution.json exists and contains the correct keys and values."""
    solution_path = "/home/user/solution.json"
    assert os.path.exists(solution_path), f"Solution file not found at {solution_path}"

    with open(solution_path, "r") as f:
        try:
            solution = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {solution_path} is not valid JSON.")

    # Ground truth values based on the numpy.random seeds specified in the task
    expected_values = {
        "bootstrap_lower": 41.7649,
        "bootstrap_upper": 42.1969,
        "k_value": 0.1732,
        "mc_mean_c5": 41.9839,
        "euler_diff": 1.2588
    }

    for key, expected_val in expected_values.items():
        assert key in solution, f"Key '{key}' is missing from solution.json."
        actual_val = solution[key]
        assert isinstance(actual_val, (int, float)), f"Value for '{key}' must be a number."

        diff = abs(actual_val - expected_val)
        assert diff <= 0.0002, (
            f"Value for '{key}' is {actual_val}, expected {expected_val} (±0.0002). "
            f"Difference is {diff:.6f}."
        )