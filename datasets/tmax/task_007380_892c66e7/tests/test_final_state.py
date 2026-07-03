# test_final_state.py

import json
import os
import pytest

def test_plot_exists():
    """Check that the plot file exists."""
    plot_path = "/home/user/mcmc_fit.png"
    assert os.path.exists(plot_path), f"Plot file not found at {plot_path}"
    assert os.path.isfile(plot_path), f"{plot_path} is not a file"

def test_results_json_exists_and_valid():
    """Check that results.json exists, has correct keys, and values are within expected ranges."""
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"Results file not found at {results_path}"
    assert os.path.isfile(results_path), f"{results_path} is not a file"

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON")

    expected_keys = {"A1_mean", "A2_mean", "A3_mean", "wasserstein_distance"}
    actual_keys = set(data.keys())
    assert expected_keys.issubset(actual_keys), f"Missing keys in results.json. Expected: {expected_keys}, Found: {actual_keys}"

    # A1 is isolated, so its mean should be very close to the least squares / true estimate (~2.01)
    a1_mean = data["A1_mean"]
    assert isinstance(a1_mean, (int, float)), "A1_mean must be a float"
    assert abs(a1_mean - 2.0) < 0.1, f"A1_mean ({a1_mean}) is not within 0.1 of 2.0"

    # The sum of A2 and A3 is constrained, and since we started at true values with small noise, 
    # they should be near 1.0 and 0.5
    a2_mean = data["A2_mean"]
    a3_mean = data["A3_mean"]
    assert isinstance(a2_mean, (int, float)), "A2_mean must be a float"
    assert isinstance(a3_mean, (int, float)), "A3_mean must be a float"

    a2_a3_sum = a2_mean + a3_mean
    assert abs(a2_a3_sum - 1.5) < 0.2, f"Sum of A2_mean and A3_mean ({a2_a3_sum}) is not within 0.2 of 1.5"

    # Wasserstein distance check
    wasserstein_distance = data["wasserstein_distance"]
    assert isinstance(wasserstein_distance, (int, float)), "wasserstein_distance must be a float"
    assert 0.0 <= wasserstein_distance < 0.05, f"wasserstein_distance ({wasserstein_distance}) is not in range [0.0, 0.05)"