# test_final_state.py
import os
import json
import pytest

def test_benchmark_script_exists():
    assert os.path.isfile("/home/user/benchmark.py"), "/home/user/benchmark.py script is missing."

def test_experiment_log_exists():
    assert os.path.isfile("/home/user/experiment_log.json"), "/home/user/experiment_log.json is missing. Did you run the script?"

def test_experiment_log_contents():
    with open("/home/user/experiment_log.json", "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/experiment_log.json is not a valid JSON file.")

    expected_keys = {"valid_shape_dtype", "mse", "max_abs_error", "true_time_ms", "approx_time_ms", "speedup"}
    assert set(results.keys()) == expected_keys, f"JSON keys do not match the expected keys. Found: {list(results.keys())}"

    assert results["valid_shape_dtype"] is True, "Validation of shape and dtype should be True."

    mse = results["mse"]
    assert isinstance(mse, float), "MSE must be a float."
    assert mse >= 0, "MSE must be >= 0."
    assert mse < 1e-10, f"MSE is abnormally high: {mse}. Check your MSE calculation."

    max_abs_error = results["max_abs_error"]
    assert isinstance(max_abs_error, float), "Max absolute error must be a float."
    assert max_abs_error >= 0, "Max absolute error must be >= 0."
    assert max_abs_error < 1e-5, f"Max absolute error is abnormally high: {max_abs_error}. Check your calculation."

    assert isinstance(results["true_time_ms"], (int, float)), "true_time_ms must be a number."
    assert results["true_time_ms"] > 0, "true_time_ms must be > 0."

    assert isinstance(results["approx_time_ms"], (int, float)), "approx_time_ms must be a number."
    assert results["approx_time_ms"] > 0, "approx_time_ms must be > 0."

    assert isinstance(results["speedup"], (int, float)), "speedup must be a number."
    assert results["speedup"] > 0, "speedup must be > 0."