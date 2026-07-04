# test_final_state.py

import os
import json
import math

def test_json_exists():
    """Check that the expected output JSON file exists."""
    assert os.path.exists("/home/user/dataset_stats.json"), "/home/user/dataset_stats.json does not exist. Did you run your script and save the output?"

def test_json_contents():
    """Check that the JSON file contains the correct keys and values within acceptable tolerances."""
    with open("/home/user/dataset_stats.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/dataset_stats.json is not a valid JSON file."

    expected_keys = {"max_error_validation", "mean_dominant_freq", "kde_at_target"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"Missing keys in JSON output: {missing_keys}"

    max_err = data["max_error_validation"]
    mean_dom = data["mean_dominant_freq"]
    kde_val = data["kde_at_target"]

    assert isinstance(max_err, (int, float)), "max_error_validation must be a number."
    assert isinstance(mean_dom, (int, float)), "mean_dominant_freq must be a number."
    assert isinstance(kde_val, (int, float)), "kde_at_target must be a number."

    # The max error should be relatively small (e.g. < 1e-4) given the tight tolerances
    assert 0 <= max_err < 1e-3, f"max_error_validation ({max_err}) is too large. Check your analytical solution and solver tolerances."

    # Mean dominant frequency should be approximately 0.77 Hz
    assert math.isclose(mean_dom, 0.77, abs_tol=0.05), f"mean_dominant_freq ({mean_dom}) is not close to the expected value (~0.77 Hz)."

    # KDE at target should be approximately 1.05
    assert math.isclose(kde_val, 1.05, abs_tol=0.1), f"kde_at_target ({kde_val}) is not close to the expected value (~1.05)."