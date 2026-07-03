# test_final_state.py

import os
import json
import pytest

def test_optimized_reports_exists():
    file_path = '/home/user/optimized_reports.json'
    assert os.path.exists(file_path), f"Expected output file '{file_path}' does not exist."

def test_optimized_reports_content():
    file_path = '/home/user/optimized_reports.json'
    assert os.path.exists(file_path), f"Expected output file '{file_path}' does not exist."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File '{file_path}' does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output must be a list of objects."

    expected_data = [
        {
            "department": "Executive",
            "manager": "Alice (CEO)",
            "reports": [
                "Bob (VP Eng)",
                "Charlie (VP Sales)",
                "Grace (HR)"
            ]
        },
        {
            "department": "Engineering",
            "manager": "Bob (VP Eng)",
            "reports": [
                "David (Eng)",
                "Eve (Eng)"
            ]
        },
        {
            "department": "Engineering",
            "manager": "David (Eng)",
            "reports": [
                "Ivan (Eng Intern)"
            ]
        },
        {
            "department": "Human Resources",
            "manager": "Grace (HR)",
            "reports": [
                "Heidi (HR Intern)"
            ]
        }
    ]

    # Check length
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} managers in the output, but found {len(data)}."

    # Check sorting and exact content
    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert "manager" in actual, f"Object at index {i} is missing the 'manager' key."
        assert "department" in actual, f"Object at index {i} is missing the 'department' key."
        assert "reports" in actual, f"Object at index {i} is missing the 'reports' key."

        assert actual["manager"] == expected["manager"], f"Expected manager '{expected['manager']}' at index {i}, got '{actual.get('manager')}'."
        assert actual["department"] == expected["department"], f"Expected department '{expected['department']}' for manager '{expected['manager']}', got '{actual.get('department')}'."

        actual_reports = actual["reports"]
        expected_reports = expected["reports"]
        assert isinstance(actual_reports, list), f"'reports' for manager '{expected['manager']}' must be a list."
        assert actual_reports == expected_reports, f"Reports for manager '{expected['manager']}' do not match expected or are not sorted correctly. Expected: {expected_reports}, Got: {actual_reports}"