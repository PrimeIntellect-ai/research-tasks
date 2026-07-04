# test_final_state.py

import os
import json
import pytest

def test_user_profiles_jsonl_exists_and_correct():
    path = "/home/user/user_profiles.jsonl"
    assert os.path.exists(path), f"Output file {path} is missing."

    expected_data = [
        {"user_id": 1, "name": "Alice", "total_post_views": 150, "second_degree_follows": [3, 4]},
        {"user_id": 2, "name": "Bob", "total_post_views": 200, "second_degree_follows": [1]},
        {"user_id": 3, "name": "Charlie", "total_post_views": 0, "second_degree_follows": [2, 5]},
        {"user_id": 4, "name": "Diana", "total_post_views": 0, "second_degree_follows": []},
        {"user_id": 5, "name": "Eve", "total_post_views": 500, "second_degree_follows": []}
    ]

    actual_data = []
    with open(path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                actual_data.append(obj)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {path} is not valid JSON: {line}")

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} lines, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual.get("user_id") == expected["user_id"], f"Line {i+1}: Expected user_id {expected['user_id']}, got {actual.get('user_id')}"
        assert actual.get("name") == expected["name"], f"Line {i+1}: Expected name {expected['name']}, got {actual.get('name')}"
        assert actual.get("total_post_views") == expected["total_post_views"], f"Line {i+1}: Expected total_post_views {expected['total_post_views']}, got {actual.get('total_post_views')}"
        assert actual.get("second_degree_follows") == expected["second_degree_follows"], f"Line {i+1}: Expected second_degree_follows {expected['second_degree_follows']}, got {actual.get('second_degree_follows')}"