# test_final_state.py
import os
import json
import math
import pytest

def test_fit_results_json_exists():
    """Verify that the fit_results.json file exists."""
    file_path = "/home/user/fit_results.json"
    assert os.path.exists(file_path), f"Missing file: {file_path}"
    assert os.path.isfile(file_path), f"Not a file: {file_path}"

def test_fit_results_values():
    """Verify that the fitted parameters are within the expected tolerances."""
    file_path = "/home/user/fit_results.json"

    try:
        with open(file_path, 'r') as f:
            res = json.load(f)
    except Exception as e:
        pytest.fail(f"Could not read or parse {file_path} as JSON: {e}")

    required_keys = ["A", "alpha", "f", "phi", "m", "c"]
    for key in required_keys:
        assert key in res, f"Missing key '{key}' in {file_path}"
        assert isinstance(res[key], (int, float)), f"Value for '{key}' must be a number"

    # Tolerances based on the verification script
    assert abs(res['f'] - 15.3) < 0.2, f"Frequency 'f' ({res['f']}) is not within tolerance of 15.3"
    assert abs(abs(res['A']) - 4.5) < 0.3, f"Amplitude 'A' ({res['A']}) is not within tolerance of 4.5"
    assert abs(res['alpha'] - 0.8) < 0.1, f"Decay rate 'alpha' ({res['alpha']}) is not within tolerance of 0.8"
    assert abs(res['m'] - 1.2) < 0.1, f"Slope 'm' ({res['m']}) is not within tolerance of 1.2"
    assert abs(res['c'] - (-0.7)) < 0.2, f"Intercept 'c' ({res['c']}) is not within tolerance of -0.7"