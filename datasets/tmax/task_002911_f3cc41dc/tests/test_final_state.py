# test_final_state.py
import os
import json
import pytest

REPORT_PATH = "/home/user/audit_report.json"

def test_audit_report_exists():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a file."

def test_audit_report_content():
    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected the JSON root to be a list, got {type(data).__name__}."
    assert len(data) == 4, f"Expected exactly 4 records in the report, got {len(data)}."

    expected_data = [
        {
            "audit_rank": 1,
            "username": "charlie",
            "assigned_role": "payment_admin"
        },
        {
            "audit_rank": 2,
            "username": "bob",
            "assigned_role": "finance_admin"
        },
        {
            "audit_rank": 3,
            "username": "eve",
            "assigned_role": "super_admin"
        },
        {
            "audit_rank": 4,
            "username": "alice",
            "assigned_role": "super_admin"
        }
    ]

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Record at index {i} is not a JSON object."

        for key in ["audit_rank", "username", "assigned_role"]:
            assert key in actual, f"Record at index {i} is missing key '{key}'."
            assert actual[key] == expected[key], f"Record at index {i} has incorrect '{key}'. Expected {expected[key]}, got {actual[key]}."

        # Check for extraneous keys
        extra_keys = set(actual.keys()) - set(expected.keys())
        assert not extra_keys, f"Record at index {i} contains unexpected keys: {extra_keys}"