# test_final_state.py

import os
import json
import pytest

def test_results_json_exists_and_valid():
    """Check that results.json exists and contains the correct schema and valid data types."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"The expected output file {results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {results_path} does not contain valid JSON.")

    expected_keys = {"gmm_weights", "regression_slope", "wasserstein_distance"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"The JSON file is missing the following keys: {missing_keys}"

    # Check GMM weights
    gmm_weights = data["gmm_weights"]
    assert isinstance(gmm_weights, list), "'gmm_weights' must be a list."
    assert len(gmm_weights) == 3, "'gmm_weights' must contain exactly 3 elements."
    assert all(isinstance(w, (int, float)) for w in gmm_weights), "All elements in 'gmm_weights' must be numbers."

    # Check if sorted descending
    assert gmm_weights == sorted(gmm_weights, reverse=True), "'gmm_weights' must be sorted in descending order."

    # Check regression slope
    assert isinstance(data["regression_slope"], (int, float)), "'regression_slope' must be a number."

    # Check wasserstein distance
    assert isinstance(data["wasserstein_distance"], (int, float)), "'wasserstein_distance' must be a number."
    assert data["wasserstein_distance"] >= 0, "'wasserstein_distance' cannot be negative."

def test_results_json_precision():
    """Check that the results are rounded to 4 decimal places where possible."""
    results_path = "/home/user/results.json"
    if not os.path.isfile(results_path):
        pytest.skip("results.json not found")

    with open(results_path, "r") as f:
        content = f.read()
        data = json.loads(content)

    # We can check the string representation to see if it has at most 4 decimal places
    # However, standard float parsing might alter this, so we just verify the parsed floats
    # don't have excessive precision beyond standard float representation of 4 decimals.
    for weight in data["gmm_weights"]:
        assert round(weight, 4) == weight, f"GMM weight {weight} is not rounded to 4 decimal places."

    assert round(data["regression_slope"], 4) == data["regression_slope"], "regression_slope is not rounded to 4 decimal places."
    assert round(data["wasserstein_distance"], 4) == data["wasserstein_distance"], "wasserstein_distance is not rounded to 4 decimal places."