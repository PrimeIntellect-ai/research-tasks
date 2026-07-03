# test_final_state.py
import os
import json
import math
import pytest

def test_experiment_results_exists():
    """Check if the experiment results JSON file was created."""
    path = "/home/user/experiment_results.json"
    assert os.path.isfile(path), f"Expected output file {path} does not exist. Ensure the ETL script writes to this exact path."

def test_experiment_results_content():
    """Validate the contents and computed metrics in the experiment results JSON."""
    path = "/home/user/experiment_results.json"

    # Check if it's valid JSON
    try:
        with open(path, 'r') as f:
            results = json.load(f)
    except Exception as e:
        pytest.fail(f"File {path} could not be read as valid JSON. Error: {e}")

    # Check for required keys
    assert "sum_projected_f1" in results, "Key 'sum_projected_f1' is missing from the JSON results."
    assert "average_posterior_mean" in results, "Key 'average_posterior_mean' is missing from the JSON results."

    # Recompute expected values based on the task description
    # Joined rows: 
    # Row 1: reading_1=10.0, reading_2=5.0, trials=10, successes=6
    # Row 2: reading_1=30.0, reading_2=15.0, trials=20, successes=15

    # Linear Algebra:
    # X1 = [10.0, 5.0], P = [[0.5, 0.2], [0.1, 0.8]] -> projected_f1 = 10.0*0.5 + 5.0*0.1 = 5.5
    # X2 = [30.0, 15.0] -> projected_f1 = 30.0*0.5 + 15.0*0.1 = 16.5
    expected_sum = 5.5 + 16.5

    # Bayesian Inference (alpha=2, beta=2):
    # Mean 1 = (2 + 6) / (2 + 2 + 10) = 8 / 14
    # Mean 2 = (2 + 15) / (2 + 2 + 20) = 17 / 24
    expected_avg = ((8 / 14) + (17 / 24)) / 2

    actual_sum = results["sum_projected_f1"]
    actual_avg = results["average_posterior_mean"]

    assert isinstance(actual_sum, (int, float)), f"'sum_projected_f1' must be a number, got {type(actual_sum)}"
    assert isinstance(actual_avg, (int, float)), f"'average_posterior_mean' must be a number, got {type(actual_avg)}"

    assert math.isclose(actual_sum, expected_sum, rel_tol=1e-5, abs_tol=1e-5), \
        f"Expected sum_projected_f1 to be {expected_sum}, but got {actual_sum}. Check the join logic and linear algebra transformation."

    assert math.isclose(actual_avg, expected_avg, rel_tol=1e-5, abs_tol=1e-5), \
        f"Expected average_posterior_mean to be {expected_avg}, but got {actual_avg}. Check the Bayesian inference calculation and averaging."