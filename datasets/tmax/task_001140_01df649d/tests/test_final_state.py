# test_final_state.py
import os
import json
import pytest

def test_process_data_script_exists():
    path = "/home/user/process_data.py"
    assert os.path.isfile(path), f"Expected script {path} is missing. Please ensure you saved your code to this location."

def test_validation_report_exists():
    path = "/home/user/validation_report.json"
    assert os.path.isfile(path), f"Expected output file {path} is missing. Did your script generate it?"

def test_validation_report_content():
    path = "/home/user/validation_report.json"
    assert os.path.isfile(path), "Validation report not found."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    expected_keys = {
        "alpha_covariance",
        "alpha_correlation",
        "beta_covariance",
        "beta_correlation",
        "alpha_valid_rows",
        "beta_valid_rows"
    }

    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"Validation report is missing keys: {missing_keys}"

    assert data["alpha_valid_rows"] == 101, f"Expected alpha_valid_rows to be 101, got {data['alpha_valid_rows']}"
    assert data["beta_valid_rows"] == 84, f"Expected beta_valid_rows to be 84, got {data['beta_valid_rows']}"

    assert abs(data["alpha_covariance"] - 11.2386) < 1e-4, f"alpha_covariance {data['alpha_covariance']} is incorrect."
    assert abs(data["alpha_correlation"] - 0.9859) < 1e-4, f"alpha_correlation {data['alpha_correlation']} is incorrect."
    assert abs(data["beta_covariance"] - (-10.9996)) < 1e-4, f"beta_covariance {data['beta_covariance']} is incorrect."
    assert abs(data["beta_correlation"] - (-0.6277)) < 1e-4, f"beta_correlation {data['beta_correlation']} is incorrect."