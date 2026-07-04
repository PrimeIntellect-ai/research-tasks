# test_final_state.py

import os
import json
import math
import pytest

RESULTS_FILE = "/home/user/results.json"

def test_results_json_exists():
    """Test that the results.json file exists."""
    assert os.path.exists(RESULTS_FILE), f"The file {RESULTS_FILE} was not created."
    assert os.path.isfile(RESULTS_FILE), f"The path {RESULTS_FILE} is not a file."

def test_results_json_values():
    """Test that the results.json file contains the correct computed values."""
    with open(RESULTS_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {RESULTS_FILE} does not contain valid JSON.")

    expected_keys = {"covariance", "posterior_mean", "posterior_variance"}
    actual_keys = set(data.keys())

    missing_keys = expected_keys - actual_keys
    assert not missing_keys, f"The JSON file is missing keys: {missing_keys}"

    # Expected values derived from the valid dataset
    expected_covariance = 0.648
    expected_post_mean = 50.51764705882353
    expected_post_var = 2.9411764705882355

    assert math.isclose(data["covariance"], expected_covariance, rel_tol=1e-3, abs_tol=1e-3), \
        f"Covariance is incorrect. Expected ~{expected_covariance}, got {data['covariance']}"

    assert math.isclose(data["posterior_mean"], expected_post_mean, rel_tol=1e-3, abs_tol=1e-3), \
        f"Posterior mean is incorrect. Expected ~{expected_post_mean}, got {data['posterior_mean']}"

    assert math.isclose(data["posterior_variance"], expected_post_var, rel_tol=1e-3, abs_tol=1e-3), \
        f"Posterior variance is incorrect. Expected ~{expected_post_var}, got {data['posterior_variance']}"