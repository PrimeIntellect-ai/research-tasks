# test_final_state.py
import os
import json
import math
import pytest

def test_posterior_results():
    results_file = "/home/user/posterior_results.json"

    # Check if the file exists
    assert os.path.exists(results_file), f"Output file {results_file} was not created."
    assert os.path.isfile(results_file), f"Path {results_file} is not a regular file."

    # Load the JSON data
    with open(results_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} is not valid JSON.")

    # Check for required keys
    required_keys = {"analytical_mean", "analytical_variance", "mcmc_mean"}
    missing_keys = required_keys - set(results.keys())
    assert not missing_keys, f"Missing required keys in JSON: {missing_keys}"

    # Known data properties from the setup
    # Data: [2, 3, 1, 4, 2, 5, 2, 3, 1, 2, 4, 3, 2, 1, 3, 2, 4, 1, 3, 2]
    n = 20
    data_sum = 50

    # Prior parameters
    alpha_prior = 2.0
    beta_prior = 1.0

    # Posterior parameters (Gamma-Poisson conjugacy)
    alpha_post = alpha_prior + data_sum
    beta_post = beta_prior + n

    expected_mean = alpha_post / beta_post
    expected_variance = alpha_post / (beta_post ** 2)

    # Validate analytical mean
    actual_analytical_mean = results["analytical_mean"]
    assert isinstance(actual_analytical_mean, (int, float)), "analytical_mean must be a number."
    assert math.isclose(actual_analytical_mean, expected_mean, rel_tol=1e-5), \
        f"Incorrect analytical_mean. Expected {expected_mean}, got {actual_analytical_mean}"

    # Validate analytical variance
    actual_analytical_variance = results["analytical_variance"]
    assert isinstance(actual_analytical_variance, (int, float)), "analytical_variance must be a number."
    assert math.isclose(actual_analytical_variance, expected_variance, rel_tol=1e-5), \
        f"Incorrect analytical_variance. Expected {expected_variance}, got {actual_analytical_variance}"

    # Validate MCMC mean (should be within 5% of analytical mean)
    actual_mcmc_mean = results["mcmc_mean"]
    assert isinstance(actual_mcmc_mean, (int, float)), "mcmc_mean must be a number."
    assert math.isclose(actual_mcmc_mean, expected_mean, rel_tol=0.05), \
        f"MCMC mean {actual_mcmc_mean} is too far from expected analytical mean {expected_mean}. " \
        "Check your MCMC sampler implementation and convergence."