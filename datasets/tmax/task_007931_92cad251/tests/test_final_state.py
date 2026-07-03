# test_final_state.py

import os
import json
import math
import pytest

RESULTS_FILE = '/home/user/results.json'

def test_results_file_exists():
    """Check if the results.json file was created."""
    assert os.path.isfile(RESULTS_FILE), f"{RESULTS_FILE} is missing. Did the script run and save the output?"

def test_results_file_content():
    """Validate the structure and values in results.json."""
    with open(RESULTS_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULTS_FILE} does not contain valid JSON.")

    assert isinstance(data, dict), f"Expected a JSON object (dictionary) in {RESULTS_FILE}."

    assert "theta_mean" in data, "The key 'theta_mean' is missing from the JSON output."
    assert "acceptance_rate" in data, "The key 'acceptance_rate' is missing from the JSON output."

    theta_mean = data["theta_mean"]
    acc_rate = data["acceptance_rate"]

    assert isinstance(theta_mean, (int, float)), "'theta_mean' must be a numeric value."
    assert isinstance(acc_rate, (int, float)), "'acceptance_rate' must be a numeric value."

    # Expected values derived from the deterministic random seed and exact MCMC procedure
    expected_theta_mean = 0.3015
    expected_acc_rate = 0.3546

    # Tolerance of 1e-3 is used to account for minor floating point differences across platforms
    assert math.isclose(theta_mean, expected_theta_mean, abs_tol=1e-3), \
        f"Expected theta_mean to be approximately {expected_theta_mean}, but got {theta_mean}. Check your MCMC logic, burn-in, and random seeding."

    assert math.isclose(acc_rate, expected_acc_rate, abs_tol=1e-3), \
        f"Expected acceptance_rate to be approximately {expected_acc_rate}, but got {acc_rate}. Ensure the acceptance criterion and proposal distributions are correct."