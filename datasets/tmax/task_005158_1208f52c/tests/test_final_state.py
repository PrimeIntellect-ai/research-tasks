# test_final_state.py

import os
import json
import math
import pytest

def test_notebook_exists():
    """Verify that the Jupyter Notebook was created."""
    notebook_path = "/home/user/fit_spectrum.ipynb"
    assert os.path.isfile(notebook_path), f"Jupyter Notebook not found at {notebook_path}"

def test_results_json_exists_and_correct():
    """Verify that the fit_results.json file exists and contains the correct values."""
    results_path = "/home/user/fit_results.json"
    assert os.path.isfile(results_path), f"Results JSON file not found at {results_path}"

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {results_path} is not valid JSON.")

    expected_keys = {"c0", "c1", "c2", "peak_area"}
    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"JSON is missing required keys: {missing_keys}"

    # Expected values from the analytical reference implementation
    expected_values = {
        "c0": 10.021040856094269,
        "c1": 1.996160867768523,
        "c2": 0.5009088647008139,
        "peak_area": 62.43319086884611
    }

    for key, expected_val in expected_values.items():
        actual_val = results[key]
        assert isinstance(actual_val, (int, float)), f"Value for {key} must be a number, got {type(actual_val)}"
        assert math.isclose(actual_val, expected_val, abs_tol=1e-4), (
            f"Value for {key} is incorrect. Expected ~{expected_val}, got {actual_val}"
        )