# test_final_state.py

import os
import json
import pytest

def test_artifacts_directory_exists():
    assert os.path.isdir('/home/user/artifacts'), "The /home/user/artifacts directory was not created."

def test_experiment_summary_exists():
    assert os.path.isfile('/home/user/artifacts/experiment_summary.json'), "The experiment_summary.json file is missing."

def test_experiment_summary_format():
    with open('/home/user/artifacts/experiment_summary.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("experiment_summary.json is not a valid JSON file.")

    assert "best_params" in data, "Missing 'best_params' in JSON output."
    assert "test_mse_ci_lower" in data, "Missing 'test_mse_ci_lower' in JSON output."
    assert "test_mse_ci_upper" in data, "Missing 'test_mse_ci_upper' in JSON output."

    assert isinstance(data["best_params"], dict), "'best_params' should be a dictionary."
    assert "max_depth" in data["best_params"], "Missing 'max_depth' in best_params."
    assert "n_estimators" in data["best_params"], "Missing 'n_estimators' in best_params."

    assert isinstance(data["test_mse_ci_lower"], (int, float)), "'test_mse_ci_lower' should be a number."
    assert isinstance(data["test_mse_ci_upper"], (int, float)), "'test_mse_ci_upper' should be a number."
    assert data["test_mse_ci_lower"] <= data["test_mse_ci_upper"], "Lower CI bound should be less than or equal to upper CI bound."

def test_experiment_summary_values():
    # Since we must use standard library only, we dynamically check that the values are within reasonable bounds
    # based on the data generation parameters (response time base is ~10 + noise + features).
    with open('/home/user/artifacts/experiment_summary.json', 'r') as f:
        data = json.load(f)

    best_params = data["best_params"]
    assert best_params["max_depth"] in [3, 5, None], f"Invalid max_depth value: {best_params['max_depth']}"
    assert best_params["n_estimators"] in [10, 50, 100], f"Invalid n_estimators value: {best_params['n_estimators']}"

    # MSE should be positive
    assert data["test_mse_ci_lower"] > 0, "MSE CI lower bound must be positive."
    assert data["test_mse_ci_upper"] > 0, "MSE CI upper bound must be positive."