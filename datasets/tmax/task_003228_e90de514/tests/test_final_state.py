# test_final_state.py

import os
import json
import math
import pytest

def test_go_source_exists():
    """Check if the Go source file was created."""
    assert os.path.isfile("/home/user/analyze_svd.go"), "/home/user/analyze_svd.go does not exist."

def test_go_mod_exists():
    """Check if the Go module was initialized."""
    assert os.path.isfile("/home/user/go.mod"), "/home/user/go.mod does not exist."

def test_results_json_exists_and_valid():
    """Check if results.json was generated and contains correct values."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"{results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} is not valid JSON.")

    expected_keys = {"mean", "ci_lower", "ci_upper"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}. Found: {set(data.keys())}"

    expected_mean = 1588.6678226065487
    expected_ci_lower = 1007.6976251214044
    expected_ci_upper = 2507.0371465910714
    tolerance = 0.001

    assert math.isclose(data["mean"], expected_mean, abs_tol=tolerance), \
        f"Expected mean to be approximately {expected_mean}, got {data['mean']}."

    assert math.isclose(data["ci_lower"], expected_ci_lower, abs_tol=tolerance), \
        f"Expected ci_lower to be approximately {expected_ci_lower}, got {data['ci_lower']}."

    assert math.isclose(data["ci_upper"], expected_ci_upper, abs_tol=tolerance), \
        f"Expected ci_upper to be approximately {expected_ci_upper}, got {data['ci_upper']}."