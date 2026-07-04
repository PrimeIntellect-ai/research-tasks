# test_final_state.py
import os
import json
import pytest

SUMMARY_PATH = "/home/user/access_summary.json"
SCRIPT_PATH = "/home/user/analyze_access.py"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def test_access_summary_exists():
    assert os.path.exists(SUMMARY_PATH), f"The output file {SUMMARY_PATH} does not exist."

def test_access_summary_content():
    with open(SUMMARY_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {SUMMARY_PATH} does not contain valid JSON.")

    expected = [
        {
            "user": "U_Alice",
            "min_hops": 4,
            "shortest_path_count": 2
        },
        {
            "user": "U_Bob",
            "min_hops": 3,
            "shortest_path_count": 1
        },
        {
            "user": "U_Charlie",
            "min_hops": 4,
            "shortest_path_count": 2
        }
    ]

    assert isinstance(data, list), f"Expected the JSON output to be a list, but got {type(data).__name__}."

    # Validate the contents
    assert len(data) == len(expected), f"Expected {len(expected)} users in the output, but found {len(data)}."

    # Ensure the list is sorted alphabetically by 'user'
    users_in_data = [item.get("user") for item in data]
    assert users_in_data == sorted(users_in_data), "The JSON array is not sorted alphabetically by the 'user' key."

    # Compare each item
    for expected_item, actual_item in zip(expected, data):
        assert actual_item.get("user") == expected_item["user"], f"Expected user {expected_item['user']}, but got {actual_item.get('user')}."
        assert actual_item.get("min_hops") == expected_item["min_hops"], f"Incorrect min_hops for {expected_item['user']}. Expected {expected_item['min_hops']}, got {actual_item.get('min_hops')}."
        assert actual_item.get("shortest_path_count") == expected_item["shortest_path_count"], f"Incorrect shortest_path_count for {expected_item['user']}. Expected {expected_item['shortest_path_count']}, got {actual_item.get('shortest_path_count')}."