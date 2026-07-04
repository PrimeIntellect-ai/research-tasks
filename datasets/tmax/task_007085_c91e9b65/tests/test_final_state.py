# test_final_state.py

import os
import json
import pytest

def test_shared_library_exists():
    """Check if the C source code was compiled into a shared library."""
    so_file = "/home/user/src/libintegrator.so"
    assert os.path.isfile(so_file), f"Shared library {so_file} is missing. Did you compile the C code?"

def test_python_script_exists():
    """Check if the preparation script exists."""
    py_file = "/home/user/prepare_data.py"
    assert os.path.isfile(py_file), f"Python script {py_file} is missing."

def test_json_output_exists():
    """Check if the regression metrics JSON file was created."""
    json_file = "/home/user/regression_metrics.json"
    assert os.path.isfile(json_file), f"Output JSON {json_file} is missing. Did you save the regression metrics?"

def test_json_contents_and_mse_values():
    """Validate the structure and values of the regression metrics JSON."""
    json_path = "/home/user/regression_metrics.json"

    with open(json_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    # Check for required keys
    expected_keys = ["mse_x", "mse_v", "mse_a"]
    for key in expected_keys:
        assert key in metrics, f"Key '{key}' is missing in the JSON output."
        assert isinstance(metrics[key], float), f"The value for '{key}' must be a float."

    # Check if the MSE values are within the expected range
    # The noise added in the golden dataset has a std dev of 1e-5, so MSE should be around 1e-10.
    mse_x = metrics["mse_x"]
    mse_v = metrics["mse_v"]
    mse_a = metrics["mse_a"]

    assert 9e-11 < mse_x < 1.1e-10, f"mse_x value {mse_x} is out of expected range (9e-11 to 1.1e-10). Check your integration or MSE calculation."
    assert 9e-11 < mse_v < 1.1e-10, f"mse_v value {mse_v} is out of expected range (9e-11 to 1.1e-10). Check your integration or MSE calculation."
    assert 9e-11 < mse_a < 1.1e-10, f"mse_a value {mse_a} is out of expected range (9e-11 to 1.1e-10). Check your acceleration derivative or MSE calculation."