# test_final_state.py
import os
import json
import pytest

def test_audit_pipeline_script_exists():
    script_path = "/home/user/audit_pipeline.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_compliance_report_exists():
    report_path = "/home/user/compliance_report.json"
    assert os.path.exists(report_path), f"The output file {report_path} does not exist."
    assert os.path.isfile(report_path), f"The path {report_path} is not a file."

def test_compliance_report_contents():
    report_path = "/home/user/compliance_report.json"
    assert os.path.exists(report_path), f"The output file {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    expected_data = [["Alice", "Bob", "Charlie"]]

    assert isinstance(data, list), "The JSON root must be a list."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} flagged cycle(s), found {len(data)}."

    assert data == expected_data, (
        f"Expected {expected_data}, but got {data}. "
        "Ensure inner lists are sorted alphabetically and the outer list is sorted lexicographically."
    )