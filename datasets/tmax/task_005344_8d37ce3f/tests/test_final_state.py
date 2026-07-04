# test_final_state.py

import os
import json
import pytest

RESULTS_PATH = '/home/user/results.json'

def test_results_file_exists():
    """Test that results.json was successfully generated."""
    assert os.path.exists(RESULTS_PATH), f"Expected results file {RESULTS_PATH} does not exist."
    assert os.path.isfile(RESULTS_PATH), f"Expected {RESULTS_PATH} to be a file."

def test_results_json_format_and_values():
    """Test that results.json has the correct structure and values within bounds."""
    assert os.path.exists(RESULTS_PATH), f"Expected results file {RESULTS_PATH} does not exist."

    with open(RESULTS_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {RESULTS_PATH} as JSON: {e}")

    assert "A_mean" in data, "Key 'A_mean' is missing from results.json"
    assert "mu_mean" in data, "Key 'mu_mean' is missing from results.json"
    assert "sse" in data, "Key 'sse' is missing from results.json"

    A_mean = data["A_mean"]
    mu_mean = data["mu_mean"]
    sse = data["sse"]

    assert isinstance(A_mean, (int, float)), f"A_mean must be a number, got {type(A_mean)}"
    assert isinstance(mu_mean, (int, float)), f"mu_mean must be a number, got {type(mu_mean)}"
    assert isinstance(sse, (int, float)), f"sse must be a number, got {type(sse)}"

    # Check bounds based on MCMC expected outcomes
    assert 4.0 <= A_mean <= 4.4, f"A_mean out of expected bounds [4.0, 4.4]: got {A_mean}"
    assert 1.2 <= mu_mean <= 1.4, f"mu_mean out of expected bounds [1.2, 1.4]: got {mu_mean}"
    assert 15.0 <= sse <= 40.0, f"sse out of expected bounds [15.0, 40.0]: got {sse}"