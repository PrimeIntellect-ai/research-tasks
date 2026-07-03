# test_final_state.py
import os
import json
import pytest

def test_fit_plot_exists():
    """Verify that the fit plot was generated."""
    plot_path = "/home/user/fit_plot.png"
    assert os.path.isfile(plot_path), f"Expected plot file not found at {plot_path}"

def test_results_json_exists_and_schema():
    """Verify that results.json exists and contains the correct schema."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Expected results file not found at {results_path}"

    with open(results_path, "r") as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    expected_keys = {"mu1", "std1", "mu2", "std2", "weight", "wasserstein_distance"}
    assert set(res.keys()) == expected_keys, f"JSON keys do not match expected schema. Found: {list(res.keys())}"

    for key in expected_keys:
        assert isinstance(res[key], (int, float)), f"Value for {key} must be a float."

def test_results_values():
    """Verify that the fitted parameters and Wasserstein distance are within expected ranges."""
    results_path = "/home/user/results.json"
    if not os.path.isfile(results_path):
        pytest.skip("results.json not found")

    with open(results_path, "r") as f:
        res = json.load(f)

    # Check mu1
    assert 1.7 <= res["mu1"] <= 2.3, f"mu1 value {res['mu1']} is out of bounds (expected ~2.0)"

    # Check mu2
    assert 7.2 <= res["mu2"] <= 7.8, f"mu2 value {res['mu2']} is out of bounds (expected ~7.5)"

    # Check std1
    assert 0.6 <= res["std1"] <= 1.0, f"std1 value {res['std1']} is out of bounds (expected ~0.8)"

    # Check std2
    assert 1.0 <= res["std2"] <= 1.4, f"std2 value {res['std2']} is out of bounds (expected ~1.2)"

    # Check weight
    assert 0.25 <= res["weight"] <= 0.45, f"weight value {res['weight']} is out of bounds (expected ~0.35)"

    # Check wasserstein_distance
    assert res["wasserstein_distance"] < 0.15, f"wasserstein_distance {res['wasserstein_distance']} is too high (expected < 0.15)"