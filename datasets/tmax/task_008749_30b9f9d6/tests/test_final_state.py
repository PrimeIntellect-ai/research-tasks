# test_final_state.py

import os
import json
import math
import pytest

def test_results_file_exists():
    assert os.path.exists("/home/user/results.json"), "The file /home/user/results.json does not exist."
    assert os.path.isfile("/home/user/results.json"), "/home/user/results.json is not a file."

def test_results_format_and_values():
    with open("/home/user/results.json", "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/results.json is not a valid JSON file.")

    expected_keys = {
        "normal_params",
        "normal_ks_distance",
        "laplace_params",
        "laplace_ks_distance",
        "best_fit"
    }

    assert set(results.keys()) == expected_keys, f"JSON keys do not match the expected keys. Found: {list(results.keys())}"

    assert isinstance(results["normal_params"], list), "normal_params must be a list"
    assert len(results["normal_params"]) == 2, "normal_params must contain exactly two elements [mu, sigma]"
    assert isinstance(results["laplace_params"], list), "laplace_params must be a list"
    assert len(results["laplace_params"]) == 2, "laplace_params must contain exactly two elements [loc, scale]"

    assert isinstance(results["normal_ks_distance"], (int, float)), "normal_ks_distance must be a number"
    assert isinstance(results["laplace_ks_distance"], (int, float)), "laplace_ks_distance must be a number"

    assert results["best_fit"] in ["Normal", "Laplace"], "best_fit must be either 'Normal' or 'Laplace'"

    # The data was generated from a Laplace distribution, so Laplace should be the best fit
    assert results["best_fit"] == "Laplace", "The best fit should be 'Laplace'"
    assert results["laplace_ks_distance"] < results["normal_ks_distance"], "Laplace KS distance should be smaller than Normal KS distance"

    # The Laplace parameters should be close to the true parameters (loc=5.0, scale=2.0)
    loc, scale = results["laplace_params"]
    assert math.isclose(loc, 5.0, abs_tol=0.5), f"Expected Laplace loc to be near 5.0, got {loc}"
    assert math.isclose(scale, 2.0, abs_tol=0.5), f"Expected Laplace scale to be near 2.0, got {scale}"

    # The KS distances should be reasonable (between 0 and 1)
    assert 0 <= results["normal_ks_distance"] <= 1, "KS distance must be between 0 and 1"
    assert 0 <= results["laplace_ks_distance"] <= 1, "KS distance must be between 0 and 1"