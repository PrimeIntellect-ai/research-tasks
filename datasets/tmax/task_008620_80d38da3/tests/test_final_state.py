# test_final_state.py

import os
import json
import pytest

JSON_PATH = '/home/user/restore_chain.json'

def test_json_file_exists():
    assert os.path.exists(JSON_PATH), f"The file {JSON_PATH} does not exist."
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} is not a regular file."

def test_json_content():
    try:
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {JSON_PATH} does not contain valid JSON.")

    expected_data = [
        {"job_id": 5, "job_name": "Full_DB_Backup_Jan1"},
        {"job_id": 12, "job_name": "Inc_DB_Backup_Jan2"},
        {"job_id": 24, "job_name": "Inc_DB_Backup_Jan3"},
        {"job_id": 45, "job_name": "Inc_DB_Backup_Jan4"},
        {"job_id": 73, "job_name": "Inc_DB_Backup_Jan5"}
    ]

    assert isinstance(data, list), "The JSON root must be a list (array)."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in the array, but found {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."
        assert "job_id" in actual, f"Item at index {i} is missing the 'job_id' key."
        assert "job_name" in actual, f"Item at index {i} is missing the 'job_name' key."
        assert len(actual.keys()) == 2, f"Item at index {i} should contain exactly two keys ('job_id' and 'job_name')."

        assert actual["job_id"] == expected["job_id"], f"Item at index {i} has incorrect 'job_id'. Expected {expected['job_id']}, got {actual['job_id']}."
        assert actual["job_name"] == expected["job_name"], f"Item at index {i} has incorrect 'job_name'. Expected '{expected['job_name']}', got '{actual['job_name']}'."