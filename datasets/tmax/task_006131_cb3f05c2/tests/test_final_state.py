# test_final_state.py

import os
import json
import pytest

def test_top_patterns_json_exists():
    file_path = "/home/user/top_patterns.json"
    assert os.path.exists(file_path), f"The output file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_top_patterns_json_content():
    file_path = "/home/user/top_patterns.json"
    assert os.path.exists(file_path), f"The output file {file_path} is missing."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    assert isinstance(data, list), f"The JSON root should be a list, but got {type(data).__name__}."
    assert len(data) == 3, f"Expected exactly 3 items in the JSON array, but got {len(data)}."

    expected_data = [
        {
            "bot_id": "n4",
            "user_id": "n5",
            "post_id": "n6",
            "total_weight": 1.6
        },
        {
            "bot_id": "n7",
            "user_id": "n8",
            "post_id": "n6",
            "total_weight": 1.4
        },
        {
            "bot_id": "n1",
            "user_id": "n2",
            "post_id": "n3",
            "total_weight": 1.3
        }
    ]

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."

        # Check keys
        expected_keys = set(expected.keys())
        actual_keys = set(actual.keys())
        assert actual_keys == expected_keys, f"Item at index {i} has keys {actual_keys}, expected {expected_keys}."

        # Check string values
        assert actual["bot_id"] == expected["bot_id"], f"Item at index {i} has bot_id {actual['bot_id']}, expected {expected['bot_id']}."
        assert actual["user_id"] == expected["user_id"], f"Item at index {i} has user_id {actual['user_id']}, expected {expected['user_id']}."
        assert actual["post_id"] == expected["post_id"], f"Item at index {i} has post_id {actual['post_id']}, expected {expected['post_id']}."

        # Check numeric value (total_weight) using a small tolerance for floating point issues
        actual_weight = actual["total_weight"]
        expected_weight = expected["total_weight"]
        assert isinstance(actual_weight, (int, float)), f"Item at index {i} total_weight is not a number."
        assert abs(actual_weight - expected_weight) < 1e-6, f"Item at index {i} has total_weight {actual_weight}, expected {expected_weight}."