# test_final_state.py

import os
import json
import pytest

def test_report_json_exists():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"The expected output file {report_path} was not created."

def test_report_json_content():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"The expected output file {report_path} was not created."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    expected_truth = {
        "day1": {
            "version": "1.0.0",
            "status": "ok"
        },
        "day2": {
            "version": "1.1.0",
            "status": "ok"
        },
        "day3": {
            "version": "",
            "status": "error_depth_exceeded"
        }
    }

    assert isinstance(report, dict), "The report should be a JSON object (dictionary)."

    for key, expected_val in expected_truth.items():
        assert key in report, f"Missing backup key '{key}' in the report."
        actual_val = report[key]
        assert isinstance(actual_val, dict), f"The value for '{key}' should be an object."
        assert actual_val.get("version") == expected_val["version"], f"Expected version '{expected_val['version']}' for '{key}', got '{actual_val.get('version')}'."
        assert actual_val.get("status") == expected_val["status"], f"Expected status '{expected_val['status']}' for '{key}', got '{actual_val.get('status')}'."

    # Ensure no extra keys are present
    for key in report.keys():
        assert key in expected_truth, f"Unexpected backup key '{key}' found in the report."