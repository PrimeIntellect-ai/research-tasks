# test_final_state.py

import os
import json
import pytest

def test_flagged_employees_json():
    json_path = "/home/user/flagged_employees.json"

    # Check if the file exists
    assert os.path.isfile(json_path), f"Expected output file {json_path} does not exist."

    # Read and parse the JSON file
    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {json_path} as valid JSON: {e}")

    # Validate structure and content
    assert isinstance(data, list), f"Expected JSON root to be a list, but got {type(data).__name__}."
    assert len(data) == 2, f"Expected exactly 2 elements in the JSON array, but got {len(data)}."

    # Validate first employee (Bob)
    expected_first = {
        "uid": 2,
        "name": "Bob",
        "in_degree": 5
    }
    assert data[0] == expected_first, f"First element in JSON does not match expected. Got {data[0]}, expected {expected_first}."

    # Validate second employee (Diana)
    expected_second = {
        "uid": 4,
        "name": "Diana",
        "in_degree": 3
    }
    assert data[1] == expected_second, f"Second element in JSON does not match expected. Got {data[1]}, expected {expected_second}."