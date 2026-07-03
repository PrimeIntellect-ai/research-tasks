# test_final_state.py

import os
import json
import pytest

VIOLATIONS_FILE = "/home/user/violations.json"

def test_violations_file_exists():
    """Test that the violations.json file was created."""
    assert os.path.isfile(VIOLATIONS_FILE), f"The file {VIOLATIONS_FILE} does not exist. Ensure your script creates it."

def test_violations_content():
    """Test that the violations.json file contains the correct violations in the correct format."""
    with open(VIOLATIONS_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {VIOLATIONS_FILE} does not contain valid JSON.")

    expected = [
        {
            "log_id": 2,
            "employee_name": "Eve",
            "resource_name": "Audit_Report_2023"
        },
        {
            "log_id": 5,
            "employee_name": "David",
            "resource_name": "Customer_PII_DB"
        }
    ]

    assert isinstance(data, list), "The JSON output must be a JSON array (list of objects)."
    assert len(data) == len(expected), f"Expected {len(expected)} violations, but found {len(data)}."

    # Validate each entry and the exact order
    for i, (actual_item, expected_item) in enumerate(zip(data, expected)):
        assert isinstance(actual_item, dict), f"Item at index {i} is not a JSON object."

        # Check keys
        actual_keys = set(actual_item.keys())
        expected_keys = set(expected_item.keys())
        assert actual_keys == expected_keys, f"Item at index {i} has incorrect keys. Expected {expected_keys}, got {actual_keys}."

        # Check values
        assert actual_item["log_id"] == expected_item["log_id"], f"Item at index {i} has incorrect log_id. Expected {expected_item['log_id']}, got {actual_item['log_id']}."
        assert actual_item["employee_name"] == expected_item["employee_name"], f"Item at index {i} has incorrect employee_name. Expected '{expected_item['employee_name']}', got '{actual_item['employee_name']}'."
        assert actual_item["resource_name"] == expected_item["resource_name"], f"Item at index {i} has incorrect resource_name. Expected '{expected_item['resource_name']}', got '{actual_item['resource_name']}'."

    assert data == expected, f"JSON content mismatch. Expected {expected}, got {data}"