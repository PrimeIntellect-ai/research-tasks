# test_final_state.py

import os
import json
import math
import pytest

def test_script_exists():
    """Check if the user script was created."""
    script_path = "/home/user/test_pca.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_report_json_exists():
    """Check if the report.json file was created."""
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

def test_report_json_content():
    """Check if report.json contains the correct max_diff value."""
    report_path = "/home/user/report.json"
    if not os.path.isfile(report_path):
        pytest.fail(f"Report file {report_path} does not exist.")

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "max_diff" in data, "Key 'max_diff' not found in report.json."
    assert len(data) == 1, "report.json should contain exactly one key."

    actual_diff = data["max_diff"]
    assert isinstance(actual_diff, float), "The value for 'max_diff' must be a float."

    expected_diff = 0.00018596616462788574
    assert math.isclose(actual_diff, expected_diff, rel_tol=1e-3), (
        f"Expected max_diff to be approx {expected_diff}, but got {actual_diff}."
    )