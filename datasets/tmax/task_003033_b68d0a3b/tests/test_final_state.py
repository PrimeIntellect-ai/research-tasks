# test_final_state.py

import os
import json
import pytest

def test_results_json_exists_and_correct():
    file_path = "/home/user/results.json"
    assert os.path.isfile(file_path), f"Missing file: {file_path}. Did you save the results to the correct path?"

    with open(file_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not a valid JSON file.")

    expected_keys = [
        "control_mean_similarity",
        "treatment_mean_similarity",
        "t_statistic",
        "p_value"
    ]

    for key in expected_keys:
        assert key in results, f"Missing key '{key}' in {file_path}."

    expected_values = {
        "control_mean_similarity": 0.1873,
        "treatment_mean_similarity": 0.4496,
        "t_statistic": -3.3768,
        "p_value": 0.0125
    }

    tolerance = 1e-3

    for key, expected_val in expected_values.items():
        actual_val = results[key]
        assert isinstance(actual_val, (int, float)), f"Value for '{key}' must be a number."
        assert abs(actual_val - expected_val) <= tolerance, (
            f"Value for '{key}' is incorrect. Expected approximately {expected_val}, but got {actual_val}. "
            f"Check your TF-IDF fitting and similarity calculations to ensure the data leak is fixed properly."
        )