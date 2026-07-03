# test_final_state.py

import os
import json
import pytest

RESULTS_FILE = '/home/user/profiling_results.json'

def test_results_file_exists():
    """Test that the profiling_results.json file exists."""
    assert os.path.isfile(RESULTS_FILE), f"The file {RESULTS_FILE} does not exist."

def test_results_json_keys():
    """Test that the results JSON contains the exact required keys."""
    with open(RESULTS_FILE, 'r') as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {RESULTS_FILE} is not valid JSON.")

    expected_keys = {"mu1", "sigma1", "mu2", "sigma2", "w1", "wasserstein_distance"}
    assert set(res.keys()) == expected_keys, f"JSON keys {set(res.keys())} do not match expected {expected_keys}."

def test_results_bounds():
    """Test that the optimized parameters and distance metric fall within acceptable bounds."""
    with open(RESULTS_FILE, 'r') as f:
        res = json.load(f)

    # Check bounds based on the ground truth distributions
    assert 0.80 <= res['w1'] <= 0.90, f"w1 out of bounds: {res['w1']}"
    assert 40.0 <= res['mu1'] <= 50.0, f"mu1 out of bounds: {res['mu1']}"
    assert 6.0 <= res['sigma1'] <= 10.0, f"sigma1 out of bounds: {res['sigma1']}"
    assert 190.0 <= res['mu2'] <= 230.0, f"mu2 out of bounds: {res['mu2']}"
    assert 30.0 <= res['sigma2'] <= 50.0, f"sigma2 out of bounds: {res['sigma2']}"
    assert 0.0 <= res['wasserstein_distance'] <= 15.0, f"wasserstein_distance out of bounds: {res['wasserstein_distance']}"

def test_component_ordering():
    """Test that component 1 represents the fast responses (lower mean)."""
    with open(RESULTS_FILE, 'r') as f:
        res = json.load(f)

    assert res['mu1'] < res['mu2'], "Components are swapped: mu1 should be less than mu2."