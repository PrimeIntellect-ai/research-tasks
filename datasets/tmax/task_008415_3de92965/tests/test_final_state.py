# test_final_state.py
import os
import json
import pytest

OUTPUT_JSON_PATH = "/home/user/graph_output.json"

def test_json_output_exists():
    """Check if the output JSON file exists."""
    assert os.path.isfile(OUTPUT_JSON_PATH), f"Output JSON file missing at {OUTPUT_JSON_PATH}"

def test_json_output_content():
    """Check if the output JSON file contains the correct hierarchy data."""
    with open(OUTPUT_JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_JSON_PATH} does not contain valid JSON.")

    expected_data = [
        {"emp_id": 1, "name": "Alice", "manager_id": None, "department": "Executive", "depth": 0},
        {"emp_id": 2, "name": "Bob", "manager_id": 1, "department": "Engineering", "depth": 1},
        {"emp_id": 3, "name": "Charlie", "manager_id": 1, "department": "Sales", "depth": 1},
        {"emp_id": 4, "name": "David", "manager_id": 2, "department": "Engineering", "depth": 2},
        {"emp_id": 5, "name": "Eve", "manager_id": 2, "department": "Engineering", "depth": 2},
        {"emp_id": 6, "name": "Frank", "manager_id": 3, "department": "Sales", "depth": 2},
        {"emp_id": 7, "name": "Grace", "manager_id": 6, "department": "Sales", "depth": 3},
        {"emp_id": 8, "name": "Heidi", "manager_id": 1, "department": "HR", "depth": 1}
    ]

    assert isinstance(data, list), "Output JSON must be a list of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(data)}."

    # The requirement specifically mentions it should be sorted by emp_id in ascending order
    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual == expected, f"Mismatch at index {i}. Expected: {expected}, Actual: {actual}"