# test_final_state.py

import os
import json
import pytest

def test_incident_report_exists():
    report_path = "/home/user/incident_report.json"
    assert os.path.isfile(report_path), f"The incident report {report_path} is missing."

def test_incident_report_content():
    report_path = "/home/user/incident_report.json"
    assert os.path.isfile(report_path), f"The incident report {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    expected_data = [
        {
            "timestamp": "2023-10-15 08:23:12",
            "decrypted_payload": "<script>alert('XSS')</script>",
            "cwe": "CWE-79"
        },
        {
            "timestamp": "2023-10-15 09:01:45",
            "decrypted_payload": "admin' OR '1'='1",
            "cwe": "CWE-89"
        },
        {
            "timestamp": "2023-10-15 10:15:30",
            "decrypted_payload": "UNION SELECT null, username--",
            "cwe": "CWE-89"
        },
        {
            "timestamp": "2023-10-15 11:42:05",
            "decrypted_payload": "<img src=x onerror=alert(1)>",
            "cwe": "CWE-79"
        }
    ]

    assert isinstance(report_data, list), "The JSON report must be a list of objects."
    assert len(report_data) == len(expected_data), f"Expected {len(expected_data)} items in the report, found {len(report_data)}."

    for i, (actual, expected) in enumerate(zip(report_data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."
        assert actual.get("timestamp") == expected["timestamp"], f"Mismatch in timestamp at index {i}."
        assert actual.get("decrypted_payload") == expected["decrypted_payload"], f"Mismatch in decrypted_payload at index {i}."
        assert actual.get("cwe") == expected["cwe"], f"Mismatch in cwe at index {i}."