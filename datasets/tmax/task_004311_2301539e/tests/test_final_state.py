# test_final_state.py

import os
import json
import pytest

def test_ci_report_exists():
    """Verify that the ci_report.json file was created."""
    report_path = "/home/user/ci_report.json"
    assert os.path.isfile(report_path), f"The file {report_path} was not created."

def test_ci_report_content():
    """Verify that the ci_report.json contains the correct evaluation results."""
    report_path = "/home/user/ci_report.json"

    try:
        with open(report_path, "r") as f:
            report_data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {report_path} does not contain valid JSON.")

    expected_data = {
        "lib-alpha": "ACCEPTED",
        "lib-beta": "REJECTED",
        "lib-gamma": "REJECTED",
        "lib-delta": "ACCEPTED",
        "lib-epsilon": "ACCEPTED"
    }

    assert isinstance(report_data, dict), "The JSON root must be a dictionary."

    for pkg, status in expected_data.items():
        assert pkg in report_data, f"Package '{pkg}' is missing from the report."
        assert report_data[pkg] == status, f"Expected '{pkg}' to be '{status}', but got '{report_data[pkg]}'."

    # Check for extra keys
    extra_keys = set(report_data.keys()) - set(expected_data.keys())
    assert not extra_keys, f"Found unexpected packages in the report: {extra_keys}"