# test_final_state.py
import os
import json
import pytest

REPORT_PATH = "/home/user/report.json"

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

def test_report_contents():
    with open(REPORT_PATH, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} does not contain valid JSON.")

    # Check db_password
    assert "db_password" in report_data, "Key 'db_password' is missing from the report."
    assert report_data["db_password"] == "pA55w0rd_xyz789", (
        f"Expected db_password to be 'pA55w0rd_xyz789', got '{report_data['db_password']}'"
    )

    # Check softmax_first_value
    assert "softmax_first_value" in report_data, "Key 'softmax_first_value' is missing from the report."

    # The true value is exp(1000) / (exp(1000)+exp(1001)+exp(1002)) 
    # = 1 / (1 + e + e^2) = 1 / (1 + 2.71828 + 7.38905) = 1 / 11.10733 = 0.09003...
    # Rounded to 4 decimal places: 0.0900
    expected_value = 0.0900
    actual_value = report_data["softmax_first_value"]

    assert isinstance(actual_value, (int, float)), "softmax_first_value must be a number."
    assert abs(actual_value - expected_value) < 1e-4, (
        f"Expected softmax_first_value to be {expected_value}, got {actual_value}"
    )