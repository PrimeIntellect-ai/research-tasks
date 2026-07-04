# test_final_state.py
import json
import os
import pytest

RESULTS_PATH = "/home/user/results.json"

def test_results_file_exists():
    """Test that the results.json file exists."""
    assert os.path.exists(RESULTS_PATH), f"{RESULTS_PATH} does not exist."
    assert os.path.isfile(RESULTS_PATH), f"{RESULTS_PATH} is not a file."

def test_results_json_structure():
    """Test that the JSON file has the exact expected keys."""
    with open(RESULTS_PATH, "r") as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON.")

    expected_keys = {
        "gmm_weights", "gmm_means", "gmm_variances", 
        "integral_value", "naive_log_likelihoods", "stable_log_likelihoods"
    }
    assert set(res.keys()) == expected_keys, f"JSON keys do not match expected. Found: {list(res.keys())}"

def test_gmm_parameters():
    """Test the extracted GMM parameters for correctness and sorting."""
    with open(RESULTS_PATH, "r") as f:
        res = json.load(f)

    weights = res["gmm_weights"]
    means = res["gmm_means"]
    variances = res["gmm_variances"]

    assert len(weights) == 2, "gmm_weights must have exactly 2 elements."
    assert len(means) == 2, "gmm_means must have exactly 2 elements."
    assert len(variances) == 2, "gmm_variances must have exactly 2 elements."

    assert all(isinstance(x, float) for x in weights), "gmm_weights must be floats."
    assert all(isinstance(x, float) for x in means), "gmm_means must be floats."
    assert all(isinstance(x, float) for x in variances), "gmm_variances must be floats."

    assert weights[0] <= weights[1], "gmm_weights must be sorted in ascending order."
    assert abs(sum(weights) - 1.0) < 1e-2, "gmm_weights should sum to approximately 1.0."

def test_integral_value():
    """Test that the integral of the PDF is approximately 1.0."""
    with open(RESULTS_PATH, "r") as f:
        res = json.load(f)

    integral = res["integral_value"]
    assert isinstance(integral, float), "integral_value must be a float."
    assert abs(integral - 1.0) < 1e-4, f"integral_value should be close to 1.0, got {integral}"

def test_naive_log_likelihoods():
    """Test that naive log likelihoods underflow to '-inf' for extreme values."""
    with open(RESULTS_PATH, "r") as f:
        res = json.load(f)

    naive = res["naive_log_likelihoods"]
    assert len(naive) == 4, "naive_log_likelihoods must have exactly 4 elements."

    assert naive[-1] == "-inf", "The most extreme outlier (1000.0) should underflow to '-inf' in the naive method."

def test_stable_log_likelihoods():
    """Test that stable log likelihoods are finite negative floats."""
    with open(RESULTS_PATH, "r") as f:
        res = json.load(f)

    stable = res["stable_log_likelihoods"]
    assert len(stable) == 4, "stable_log_likelihoods must have exactly 4 elements."

    assert all(isinstance(x, float) for x in stable), "All elements in stable_log_likelihoods must be floats."
    assert all(x < 0 for x in stable), "All log likelihoods should be negative."
    assert stable[-1] < -10000, f"Expected last stable log likelihood to be < -10000 (no underflow to -inf), got {stable[-1]}"