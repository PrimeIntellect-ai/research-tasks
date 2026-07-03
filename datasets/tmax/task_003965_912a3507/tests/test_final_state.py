# test_final_state.py

import os
import json
import pytest

RESULTS_PATH = "/home/user/results.json"
EVALUATE_SCRIPT_PATH = "/home/user/evaluate.py"

def test_evaluate_script_exists():
    """Test that the student created the evaluate.py script."""
    assert os.path.exists(EVALUATE_SCRIPT_PATH), f"Missing script: {EVALUATE_SCRIPT_PATH}"
    assert os.path.isfile(EVALUATE_SCRIPT_PATH), f"Path is not a file: {EVALUATE_SCRIPT_PATH}"

def test_results_json_exists():
    """Test that the results.json file was generated."""
    assert os.path.exists(RESULTS_PATH), f"Missing results file: {RESULTS_PATH}"
    assert os.path.isfile(RESULTS_PATH), f"Path is not a file: {RESULTS_PATH}"

def test_results_json_schema_and_types():
    """Test that results.json contains the exact required keys and float values."""
    with open(RESULTS_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} is not valid JSON.")

    expected_keys = {"fixed_mse", "mse_std_err", "corr_A_B", "avg_inference_us"}
    actual_keys = set(data.keys())

    missing = expected_keys - actual_keys
    extra = actual_keys - expected_keys

    assert not missing, f"results.json is missing keys: {missing}"
    assert not extra, f"results.json has unexpected keys: {extra}"

    for key in expected_keys:
        val = data[key]
        assert isinstance(val, (int, float)), f"Value for '{key}' must be a float, got {type(val).__name__}"

def test_results_plausible_values():
    """Test that the metrics in results.json are within plausible ranges."""
    with open(RESULTS_PATH, "r") as f:
        data = json.load(f)

    assert data["fixed_mse"] > 0, "MSE should be strictly positive."
    assert data["mse_std_err"] > 0, "MSE standard error should be strictly positive."
    assert -1.0 <= data["corr_A_B"] <= 1.0, "Pearson correlation must be between -1 and 1."
    assert data["avg_inference_us"] > 0, "Average inference time must be strictly positive."