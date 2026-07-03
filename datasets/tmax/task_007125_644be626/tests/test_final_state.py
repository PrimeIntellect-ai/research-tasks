# test_final_state.py

import os
import json
import pytest

def test_output_json_exists():
    file_path = "/home/user/output.json"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing. Did the script run successfully?"

def test_output_json_content():
    file_path = "/home/user/output.json"

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected_data = [
        {
            "ID": "1",
            "Name": "Alice",
            "Email": "alice@example.com",
            "Comments": "Good customer"
        },
        {
            "ID": "3",
            "Name": "Charlie",
            "Email": "charlie@example.com",
            "Comments": "Standard tier"
        },
        {
            "ID": "5",
            "Name": "Dave",
            "Email": "dave@example.com",
            "Comments": "Normal row"
        },
        {
            "ID": "7",
            "Name": "Frank",
            "Email": "frank@example.com",
            "Comments": "Another good customer"
        }
    ]

    assert isinstance(data, list), "Output JSON must be an array of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} rows in output, but got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual == expected, f"Row {i} in output JSON does not match expected data.\nExpected: {expected}\nActual: {actual}"