# test_final_state.py

import os
import json
import pytest

JSON_PATH = "/home/user/salary_rollup.json"

def test_json_file_exists():
    """Check if the output JSON file exists."""
    assert os.path.exists(JSON_PATH), f"Output file missing at {JSON_PATH}"
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} is not a file"

def test_json_content_and_structure():
    """Check if the JSON file has the correct structure and values."""
    assert os.path.exists(JSON_PATH), f"Output file missing at {JSON_PATH}"

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {JSON_PATH} as JSON: {e}")

    assert isinstance(data, list), "JSON root must be a list (array)."
    assert len(data) == 7, f"Expected 7 employee records, found {len(data)}."

    expected_data = [
        {"id": 1, "name": "Alice", "total_salary": 515000.00},
        {"id": 2, "name": "Bob", "total_salary": 205000.00},
        {"id": 3, "name": "Charlie", "total_salary": 210000.00},
        {"id": 4, "name": "Dave", "total_salary": 60000.00},
        {"id": 5, "name": "Eve", "total_salary": 65000.00},
        {"id": 6, "name": "Frank", "total_salary": 120000.00},
        {"id": 7, "name": "Grace", "total_salary": 50000.00},
    ]

    for i, expected in enumerate(expected_data):
        actual = data[i]
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."

        # Check keys
        assert "id" in actual, f"Missing 'id' key in item at index {i}."
        assert "name" in actual, f"Missing 'name' key in item at index {i}."
        assert "total_salary" in actual, f"Missing 'total_salary' key in item at index {i}."

        # Check values
        assert actual["id"] == expected["id"], f"Expected id {expected['id']} at index {i}, got {actual['id']}."
        assert actual["name"] == expected["name"], f"Expected name {expected['name']} at index {i}, got {actual['name']}."

        # Check total_salary (allowing small floating point differences, though it should be exact or formatted to 2 decimals)
        actual_salary = float(actual["total_salary"])
        expected_salary = expected["total_salary"]
        assert abs(actual_salary - expected_salary) < 0.01, \
            f"Expected total_salary {expected_salary} for id {expected['id']}, got {actual_salary}."