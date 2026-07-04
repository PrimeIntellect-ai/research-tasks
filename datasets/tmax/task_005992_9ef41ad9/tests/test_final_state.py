# test_final_state.py

import os
import json
import math

def test_run_analysis_script_exists_and_executable():
    """Test that the run_analysis.sh script exists and is executable."""
    script_path = "/home/user/run_analysis.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_results_json_exists():
    """Test that the results.json file exists."""
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"The file {results_path} does not exist. The script might not have generated it."
    assert os.path.isfile(results_path), f"The path {results_path} is not a file."

def test_results_json_content():
    """Test that results.json contains the correct keys and values within tolerance."""
    results_path = "/home/user/results.json"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {results_path} does not contain valid JSON."

    expected_keys = ["correlation", "bootstrap_ci_5th", "bootstrap_ci_95th", "best_alpha"]
    for key in expected_keys:
        assert key in results, f"Key '{key}' is missing from {results_path}."

    expected_values = {
        "correlation": 0.7788,
        "bootstrap_ci_5th": 0.7570,
        "bootstrap_ci_95th": 0.7998,
        "best_alpha": 10.0
    }

    tolerance = 0.0002

    for key, expected in expected_values.items():
        actual = results[key]
        assert isinstance(actual, (int, float)), f"Value for '{key}' should be a number."
        assert math.isclose(actual, expected, abs_tol=tolerance), \
            f"Value for '{key}' is {actual}, expected {expected} (within +/- {tolerance})."