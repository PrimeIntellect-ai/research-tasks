# test_final_state.py

import os
import json
import pytest

RESULTS_PATH = "/home/user/workspace/results.json"

def test_results_file_exists():
    assert os.path.exists(RESULTS_PATH), f"File {RESULTS_PATH} does not exist."
    assert os.path.isfile(RESULTS_PATH), f"Path {RESULTS_PATH} is not a file."

def test_results_json_content():
    assert os.path.exists(RESULTS_PATH), f"File {RESULTS_PATH} does not exist."
    with open(RESULTS_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} is not valid JSON.")

    expected_keys = {"refined_N", "integral_error", "derivative_estimate", "ci_lower", "ci_upper"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"Missing keys in results.json: {missing_keys}"

    assert data["refined_N"] == 256, f"Expected refined_N to be 256, got {data['refined_N']}"
    assert 0.000030 <= data["integral_error"] <= 0.000035, f"Expected integral_error between 0.000030 and 0.000035, got {data['integral_error']}"
    assert 0.870 <= data["derivative_estimate"] <= 0.878, f"Expected derivative_estimate between 0.870 and 0.878, got {data['derivative_estimate']}"
    assert -8.5 <= data["ci_lower"] <= -7.5, f"Expected ci_lower between -8.5 and -7.5, got {data['ci_lower']}"
    assert 9.2 <= data["ci_upper"] <= 10.2, f"Expected ci_upper between 9.2 and 10.2, got {data['ci_upper']}"