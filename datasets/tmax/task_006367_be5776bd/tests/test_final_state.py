# test_final_state.py

import os
import json
import pytest

RESULTS_PATH = "/home/user/results.json"

def test_results_file_exists():
    """Check that the results.json file exists."""
    assert os.path.isfile(RESULTS_PATH), f"File {RESULTS_PATH} is missing. The script did not generate the output."

def test_results_valid_json():
    """Check that results.json is valid JSON and a dictionary."""
    with open(RESULTS_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} is not valid JSON.")

    assert isinstance(data, dict), f"JSON content in {RESULTS_PATH} must be a dictionary."

def test_results_keys_and_types():
    """Check that results.json contains exactly the required keys with correct types."""
    with open(RESULTS_PATH, 'r') as f:
        data = json.load(f)

    expected_keys = {
        "n_components",
        "best_alpha",
        "baseline_mean_mse",
        "pca_mean_mse",
        "p_value",
        "ci_lower",
        "ci_upper"
    }

    actual_keys = set(data.keys())
    missing_keys = expected_keys - actual_keys
    extra_keys = actual_keys - expected_keys

    assert not missing_keys, f"Missing keys in results.json: {missing_keys}"
    assert not extra_keys, f"Extra keys in results.json: {extra_keys}"

    assert isinstance(data["n_components"], int) or (isinstance(data["n_components"], float) and data["n_components"].is_integer()), "n_components must be an integer."
    assert isinstance(data["best_alpha"], (int, float)), "best_alpha must be a float."
    assert isinstance(data["baseline_mean_mse"], (int, float)), "baseline_mean_mse must be a float."
    assert isinstance(data["pca_mean_mse"], (int, float)), "pca_mean_mse must be a float."
    assert isinstance(data["p_value"], (int, float)), "p_value must be a float."
    assert isinstance(data["ci_lower"], (int, float)), "ci_lower must be a float."
    assert isinstance(data["ci_upper"], (int, float)), "ci_upper must be a float."

def test_results_value_invariants():
    """Check that the values in results.json satisfy logical invariants."""
    with open(RESULTS_PATH, 'r') as f:
        data = json.load(f)

    # n_components should be between 1 and 20 (max features)
    assert 1 <= data["n_components"] <= 20, f"n_components ({data['n_components']}) is out of expected bounds [1, 20]."

    # best_alpha should be one of the grid search values
    valid_alphas = {0.1, 1.0, 10.0, 100.0}
    # Allow for small floating point differences
    assert any(abs(data["best_alpha"] - a) < 1e-6 for a in valid_alphas), f"best_alpha ({data['best_alpha']}) is not one of the expected grid values [0.1, 1.0, 10.0, 100.0]."

    # MSEs should be positive
    assert data["baseline_mean_mse"] >= 0, "baseline_mean_mse must be non-negative."
    assert data["pca_mean_mse"] >= 0, "pca_mean_mse must be non-negative."

    # p-value should be a valid probability
    assert 0.0 <= data["p_value"] <= 1.0, f"p_value ({data['p_value']}) must be between 0 and 1."

    # Confidence interval lower bound should be <= upper bound
    assert data["ci_lower"] <= data["ci_upper"], f"ci_lower ({data['ci_lower']}) must be <= ci_upper ({data['ci_upper']})."