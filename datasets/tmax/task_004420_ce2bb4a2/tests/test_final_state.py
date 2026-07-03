# test_final_state.py

import os
import json
import pytest

def test_virtual_environment_exists():
    """Verify that the virtual environment was created."""
    venv_python = '/home/user/etl_env/bin/python'
    assert os.path.isfile(venv_python) or os.path.isfile('/home/user/etl_env/bin/python3'), \
        "Python virtual environment was not created properly at /home/user/etl_env."

def test_script_exists_and_configured():
    """Verify the script exists and contains the required numpy configuration."""
    script_path = '/home/user/pipeline/quality_check.py'
    assert os.path.isfile(script_path), f"The script was not found at {script_path}."

    with open(script_path, 'r') as f:
        content = f.read()

    # Check for the numpy configuration
    assert "seterr" in content and "divide" in content and "raise" in content, \
        "The script does not seem to configure numpy to raise an error on division by zero."

def test_report_json_matches_expected():
    """Verify the report.json matches the expected structure and computed values."""
    report_path = '/home/user/pipeline/report.json'
    expected_path = '/tmp/expected_report.json'

    assert os.path.isfile(report_path), f"The output report was not found at {report_path}."
    assert os.path.isfile(expected_path), f"The expected report was not found at {expected_path}."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file at {report_path} is not valid JSON.")

    with open(expected_path, 'r') as f:
        expected = json.load(f)

    expected_keys = ["best_alpha", "cv_best_score", "new_revenue_mean_ci", "t_test_p_value", "data_drift_detected"]
    for key in expected_keys:
        assert key in report, f"Missing required key '{key}' in report.json."

        expected_val = expected[key]
        actual_val = report[key]

        if isinstance(expected_val, float):
            assert isinstance(actual_val, (int, float)), f"Value for '{key}' must be a float."
            assert abs(actual_val - expected_val) <= 1e-4, \
                f"Value for '{key}' is incorrect. Expected {expected_val}, got {actual_val}."
        elif isinstance(expected_val, list):
            assert isinstance(actual_val, list) and len(actual_val) == 2, \
                f"Value for '{key}' must be a list of two floats."
            for a, e in zip(actual_val, expected_val):
                assert abs(a - e) <= 1e-4, \
                    f"List values for '{key}' are incorrect. Expected {expected_val}, got {actual_val}."
        elif isinstance(expected_val, bool):
            assert isinstance(actual_val, bool), f"Value for '{key}' must be a boolean."
            assert actual_val == expected_val, \
                f"Value for '{key}' is incorrect. Expected {expected_val}, got {actual_val}."