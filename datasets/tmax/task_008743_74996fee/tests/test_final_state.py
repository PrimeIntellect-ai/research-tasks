# test_final_state.py
import os
import json
import pytest

REPORT_PATH = "/home/user/redteam_report.json"

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"The report file {REPORT_PATH} does not exist."

def test_report_is_valid_json():
    with open(REPORT_PATH, 'r') as f:
        try:
            json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON.")

def test_report_content_redacted():
    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    assert "status" in data, "The 'status' key is missing from the JSON response."
    assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'."

    assert "data" in data, "The 'data' key is missing from the JSON response."
    assert isinstance(data["data"], list), "The 'data' value should be a list."

    expected_data = [
        {"id": 1, "name": "Alice CEO", "ssn": "***-**-****", "access": "full"},
        {"id": 2, "name": "Bob CTO", "ssn": "***-**-****", "access": "full"},
        {"id": 3, "name": "Charlie CFO", "ssn": "***-**-****", "access": "full"}
    ]

    assert len(data["data"]) == len(expected_data), f"Expected {len(expected_data)} records, got {len(data['data'])}."

    for i, record in enumerate(data["data"]):
        assert record == expected_data[i], f"Record at index {i} does not match the expected redacted output. Got: {record}"