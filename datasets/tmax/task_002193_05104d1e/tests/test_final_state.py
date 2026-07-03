# test_final_state.py

import os
import json
import pytest

def test_go_file_exists():
    go_file = "/home/user/analyze.go"
    assert os.path.exists(go_file), f"Expected Go source file {go_file} is missing."
    assert os.path.isfile(go_file), f"{go_file} is not a regular file."

def test_json_output_exists_and_correct():
    json_file = "/home/user/valid_restore_points.json"
    assert os.path.exists(json_file), f"Expected output file {json_file} is missing."
    assert os.path.isfile(json_file), f"{json_file} is not a regular file."

    with open(json_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {json_file} as JSON: {e}")

    assert isinstance(data, list), f"Expected JSON root to be a list, got {type(data).__name__}."

    expected = [
        {"id": "B01", "materialized_size": 5000},
        {"id": "B02", "materialized_size": 5500},
        {"id": "B03", "materialized_size": 5750},
        {"id": "D01", "materialized_size": 6000},
        {"id": "D02", "materialized_size": 6600}
    ]

    # Check that the data exactly matches the expected output
    assert data == expected, f"JSON output does not match expected valid restore points.\nExpected: {expected}\nGot: {data}"

    # Check sorting explicitly
    ids = [item.get("id") for item in data]
    assert ids == sorted(ids), "The JSON array is not sorted by 'id' in ascending alphabetical order."