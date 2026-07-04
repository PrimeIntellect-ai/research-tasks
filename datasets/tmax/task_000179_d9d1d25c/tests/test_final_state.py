# test_final_state.py

import os
import json
import math
import pytest

def test_shared_library_compiled():
    """Test that the C code was compiled into a shared library."""
    lib_path = "/home/user/src/libnaive.so"
    assert os.path.exists(lib_path), f"{lib_path} does not exist. Did you compile the C code?"
    assert os.path.isfile(lib_path), f"{lib_path} is not a file."
    assert os.access(lib_path, os.R_OK), f"{lib_path} is not readable."

def test_results_json_exists_and_valid():
    """Test that results.json exists and contains the correct keys and valid values."""
    json_path = "/home/user/results.json"
    assert os.path.exists(json_path), f"{json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not a valid JSON file.")

    expected_keys = {
        "unstable_residual_norm",
        "stable_ridge_mse",
        "mse_ci_lower",
        "mse_ci_upper"
    }

    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"results.json is missing keys: {missing_keys}"

    # Validate types
    for key in expected_keys:
        val = results[key]
        assert isinstance(val, (int, float)), f"Value for {key} must be a float, got {type(val)}."

def test_results_values():
    """Test that the numerical values in results.json match the expected ground truth."""
    json_path = "/home/user/results.json"
    if not os.path.exists(json_path):
        pytest.skip("results.json not found")

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("results.json is not valid JSON")

    unstable_norm = results.get("unstable_residual_norm")
    stable_mse = results.get("stable_ridge_mse")
    ci_lower = results.get("mse_ci_lower")
    ci_upper = results.get("mse_ci_upper")

    # Check unstable_residual_norm
    if unstable_norm is not None:
        is_large = (isinstance(unstable_norm, float) and (math.isnan(unstable_norm) or math.isinf(unstable_norm))) or \
                   (unstable_norm > 100)
        assert is_large, f"unstable_residual_norm should be > 100 or NaN/Inf, got {unstable_norm}"

    # Check stable_ridge_mse
    if stable_mse is not None:
        assert 0.30 <= stable_mse <= 0.31, f"stable_ridge_mse should be between 0.30 and 0.31, got {stable_mse}"

    # Check mse_ci_lower
    if ci_lower is not None:
        assert 0.22 <= ci_lower <= 0.25, f"mse_ci_lower should be between 0.22 and 0.25, got {ci_lower}"

    # Check mse_ci_upper
    if ci_upper is not None:
        assert 0.37 <= ci_upper <= 0.40, f"mse_ci_upper should be between 0.37 and 0.40, got {ci_upper}"