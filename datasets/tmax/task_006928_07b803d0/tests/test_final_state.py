# test_final_state.py
import os
import json
import pytest

def test_report_json_exists_and_correct():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Expected output file missing: {report_path}"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {report_path}")

    assert isinstance(data, list), "The report should be a JSON array (list)."
    assert len(data) == 2, f"Expected exactly 2 records in the report, found {len(data)}."

    expected_records = [
        {
            "project_name": "Apollo",
            "lead_name": "Alice",
            "department_name": "Engineering",
            "direct_reports": 2,
            "risk_level": "High"
        },
        {
            "project_name": "Hermes",
            "lead_name": "Diana",
            "department_name": "HR",
            "direct_reports": 1,
            "risk_level": "Low"
        }
    ]

    # Since order doesn't matter, we can sort both lists of dicts by project_name
    def sort_key(record):
        return record.get("project_name", "")

    sorted_data = sorted(data, key=sort_key)
    sorted_expected = sorted(expected_records, key=sort_key)

    for i, (actual, expected) in enumerate(zip(sorted_data, sorted_expected)):
        assert actual == expected, f"Record mismatch. Expected {expected}, but got {actual}"