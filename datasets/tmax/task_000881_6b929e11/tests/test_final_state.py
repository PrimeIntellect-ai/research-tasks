# test_final_state.py

import os
import json
import pytest

def test_audit_script_exists():
    script_path = "/home/user/audit.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_violations_json_exists():
    output_path = "/home/user/violations.json"
    assert os.path.isfile(output_path), f"The output file {output_path} was not generated."

def test_violations_json_content():
    output_path = "/home/user/violations.json"
    assert os.path.isfile(output_path), f"The output file {output_path} is missing."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} does not contain valid JSON.")

    assert isinstance(data, list), f"The JSON in {output_path} must be a list of objects."

    expected_data = [
        {
            "user_id": "u101",
            "name": "Alice Smith",
            "entry_node": "A",
            "target_node": "F",
            "path_length": 2
        },
        {
            "user_id": "u104",
            "name": "Diana Prince",
            "entry_node": "E",
            "target_node": "F",
            "path_length": 3
        }
    ]

    # Sort both lists by user_id to ensure order doesn't cause a false failure
    # even though the instructions say it should be sorted alphabetically by user_id.
    sorted_data = sorted(data, key=lambda x: x.get("user_id", ""))
    sorted_expected = sorted(expected_data, key=lambda x: x["user_id"])

    assert sorted_data == sorted_expected, f"The contents of {output_path} do not match the expected violations and path lengths."

def test_violations_json_is_sorted():
    output_path = "/home/user/violations.json"
    if not os.path.isfile(output_path):
        pytest.skip(f"{output_path} missing")

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Invalid JSON")

    if isinstance(data, list):
        user_ids = [item.get("user_id", "") for item in data]
        assert user_ids == sorted(user_ids), f"The array in {output_path} is not sorted alphabetically by user_id."