# test_final_state.py
import os
import json
import math
import pytest

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script file missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Results file missing: {results_path}"

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} does not contain valid JSON.")

    expected_correlation = 0.9989
    expected_slope = 0.1060
    expected_intercept = -2.7900

    assert "correlation" in data, "Missing 'correlation' key in results.json"
    assert "slope" in data, "Missing 'slope' key in results.json"
    assert "intercept" in data, "Missing 'intercept' key in results.json"

    assert math.isclose(float(data["correlation"]), expected_correlation, abs_tol=0.00015), \
        f"Expected correlation close to {expected_correlation}, got {data['correlation']}"
    assert math.isclose(float(data["slope"]), expected_slope, abs_tol=0.00015), \
        f"Expected slope close to {expected_slope}, got {data['slope']}"
    assert math.isclose(float(data["intercept"]), expected_intercept, abs_tol=0.00015), \
        f"Expected intercept close to {expected_intercept}, got {data['intercept']}"