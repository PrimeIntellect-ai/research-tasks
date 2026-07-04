# test_final_state.py
import os
import json
import pytest

def test_summary_json_correctness():
    """Test that the summary.json file matches the expected output exactly."""
    summary_path = "/home/user/summary.json"

    assert os.path.isfile(summary_path), f"Output file {summary_path} does not exist. Did you run the script?"

    with open(summary_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} does not contain valid JSON.")

    expected_data = [
        {"name": "Alice", "total_spent": 135},
        {"name": "Charlie", "total_spent": 20},
        {"name": "David", "total_spent": 210}
    ]

    assert isinstance(data, list), f"Expected a JSON array, but got {type(data).__name__}"
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, but got {len(data)}"

    # Check exact match including order
    assert data == expected_data, f"Data in {summary_path} does not match expected output.\nExpected: {expected_data}\nGot: {data}"