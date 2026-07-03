# test_final_state.py
import os
import json
import pytest

JSON_PATH = "/home/user/audit_chain.json"

def test_audit_chain_json_exists():
    assert os.path.exists(JSON_PATH), f"Output file missing at {JSON_PATH}"
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} is not a file"

def test_audit_chain_json_content():
    with open(JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{JSON_PATH} does not contain valid JSON")

    expected_data = [
        {
            "level": 0,
            "employee_id": 845,
            "employee_name": "Eve Engineer",
            "department_name": "Engineering",
            "manager_id": 404
        },
        {
            "level": 1,
            "employee_id": 404,
            "employee_name": "Diana Manager",
            "department_name": "Engineering",
            "manager_id": 42
        },
        {
            "level": 2,
            "employee_id": 42,
            "employee_name": "Charlie Director",
            "department_name": "Engineering",
            "manager_id": 10
        },
        {
            "level": 3,
            "employee_id": 10,
            "employee_name": "Bob VP",
            "department_name": "Operations",
            "manager_id": 1
        },
        {
            "level": 4,
            "employee_id": 1,
            "employee_name": "Alice CEO",
            "department_name": "Executive",
            "manager_id": None
        }
    ]

    assert isinstance(data, list), "JSON output should be a list of objects"
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, got {len(data)}"

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a dictionary"
        for key, expected_val in expected.items():
            assert key in actual, f"Missing key '{key}' in item at index {i}"
            assert actual[key] == expected_val, f"Mismatch for key '{key}' at index {i}: expected {expected_val}, got {actual[key]}"