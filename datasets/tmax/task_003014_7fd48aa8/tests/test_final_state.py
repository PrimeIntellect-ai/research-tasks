# test_final_state.py

import os
import json
import math
import pytest

def test_analysis_results_exists_and_valid():
    file_path = '/home/user/analysis_results.json'

    assert os.path.exists(file_path), f"The file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    expected_keys = {"max_diff", "sse_A", "sse_B", "aic_A", "aic_B", "best_model"}
    assert set(data.keys()) == expected_keys, f"Expected keys {expected_keys}, but got {set(data.keys())}."

    assert isinstance(data["max_diff"], (int, float)), "max_diff must be a float"
    assert isinstance(data["sse_A"], (int, float)), "sse_A must be a float"
    assert isinstance(data["sse_B"], (int, float)), "sse_B must be a float"
    assert isinstance(data["aic_A"], (int, float)), "aic_A must be a float"
    assert isinstance(data["aic_B"], (int, float)), "aic_B must be a float"
    assert isinstance(data["best_model"], str), "best_model must be a string"

def test_analysis_results_logic():
    file_path = '/home/user/analysis_results.json'
    with open(file_path, 'r') as f:
        data = json.load(f)

    # The RK45 numerical solution should be very close to the analytical solution
    assert 0.0 <= data["max_diff"] < 1.0, f"max_diff is {data['max_diff']}, which is unusually large for RK45 vs Analytical."

    # Model B (Logistic) should fit the data much better than Model A (Exponential)
    assert data["sse_B"] < data["sse_A"], "SSE for Model B should be less than SSE for Model A."

    # AIC for Model B should be lower
    assert data["aic_B"] < data["aic_A"], "AIC for Model B should be less than AIC for Model A."

    # Best model should be B
    assert data["best_model"] == "B", f"Expected best_model to be 'B', got '{data['best_model']}'."

    # Check that AIC values are consistent with SSE values
    n = 101 # number of data points
    expected_aic_A = n * math.log(data["sse_A"] / n) + 2 * 1
    expected_aic_B = n * math.log(data["sse_B"] / n) + 2 * 2

    assert abs(data["aic_A"] - expected_aic_A) < 0.1, f"aic_A is inconsistent with sse_A. Expected approx {expected_aic_A}, got {data['aic_A']}"
    assert abs(data["aic_B"] - expected_aic_B) < 0.1, f"aic_B is inconsistent with sse_B. Expected approx {expected_aic_B}, got {data['aic_B']}"