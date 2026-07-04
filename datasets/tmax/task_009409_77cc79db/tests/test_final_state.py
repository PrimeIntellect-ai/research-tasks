# test_final_state.py

import os
import json
import pytest

def test_top_communicators_json_exists():
    file_path = "/home/user/top_communicators.json"
    assert os.path.isfile(file_path), f"Expected output file {file_path} is missing."

def test_top_communicators_json_content():
    file_path = "/home/user/top_communicators.json"
    assert os.path.isfile(file_path), f"Expected output file {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected_data = [
        {
            "department": "Engineering",
            "emp_id": 3,
            "name": "Charlie",
            "interaction_count": 4
        },
        {
            "department": "Engineering",
            "emp_id": 4,
            "name": "David",
            "interaction_count": 2
        },
        {
            "department": "HR",
            "emp_id": 6,
            "name": "Frank",
            "interaction_count": 2
        },
        {
            "department": "HR",
            "emp_id": 7,
            "name": "Grace",
            "interaction_count": 0
        },
        {
            "department": "Sales",
            "emp_id": 1,
            "name": "Alice",
            "interaction_count": 4
        },
        {
            "department": "Sales",
            "emp_id": 2,
            "name": "Bob",
            "interaction_count": 2
        }
    ]

    assert isinstance(data, list), "Output JSON must be a list of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, but got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."
        assert actual == expected, f"Item at index {i} does not match expected output.\nExpected: {expected}\nActual: {actual}"