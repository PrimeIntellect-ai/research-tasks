# test_final_state.py

import os
import json
import pytest

JSON_PATH = '/home/user/influencer_metrics.json'

def test_json_file_exists():
    """Test that the output JSON file exists."""
    assert os.path.isfile(JSON_PATH), f"Output file missing at {JSON_PATH}"

def test_json_contents_correct():
    """Test that the JSON file contains the correct data and sorting."""
    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {JSON_PATH} is not valid JSON")

    assert isinstance(data, list), "JSON root must be a list of dictionaries"

    expected_data = [
        {
            "user_id": 4,
            "name": "Diana",
            "degree": 3,
            "total_engagements": 150
        },
        {
            "user_id": 3,
            "name": "Charlie",
            "degree": 2,
            "total_engagements": 75
        },
        {
            "user_id": 1,
            "name": "Alice",
            "degree": 3,
            "total_engagements": 45
        },
        {
            "user_id": 2,
            "name": "Bob",
            "degree": 2,
            "total_engagements": 7
        },
        {
            "user_id": 6,
            "name": "Frank",
            "degree": 2,
            "total_engagements": 3
        }
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(data)}"

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a dictionary"

        # Check keys
        expected_keys = {"user_id", "name", "degree", "total_engagements"}
        assert set(actual.keys()) == expected_keys, f"Item at index {i} has incorrect keys. Expected {expected_keys}, found {set(actual.keys())}"

        # Check values
        assert actual["user_id"] == expected["user_id"], f"Item at index {i} has wrong user_id. Expected {expected['user_id']}, got {actual['user_id']}"
        assert actual["name"] == expected["name"], f"Item at index {i} has wrong name. Expected '{expected['name']}', got '{actual['name']}'"
        assert actual["degree"] == expected["degree"], f"Item at index {i} has wrong degree. Expected {expected['degree']}, got {actual['degree']}"
        assert actual["total_engagements"] == expected["total_engagements"], f"Item at index {i} has wrong total_engagements. Expected {expected['total_engagements']}, got {actual['total_engagements']}"