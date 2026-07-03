# test_final_state.py

import os
import json
import re
from collections import defaultdict, Counter

def get_expected_features(raw_logs_path):
    if not os.path.isfile(raw_logs_path):
        return {}

    records = []

    # [INFO] 2023-10-01T12:00:01Z - User: U001 performed Action: VIEW on Item: I001. Status: SUCCESS
    pattern = re.compile(
        r'^\[.*?\]\s+(?P<timestamp>\S+)\s+-\s+User:\s+(?P<user_id>\S+)\s+performed\s+Action:\s+(?P<action>\S+)\s+on\s+Item:\s+(?P<item_id>\S+?)\.?\s+Status:\s+(?P<status>\S+)\s*$'
    )

    with open(raw_logs_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            if match:
                status = match.group('status').upper()
                if status == 'SUCCESS':
                    timestamp = match.group('timestamp')
                    user_id = match.group('user_id').upper()
                    action = match.group('action').upper()
                    item_id = match.group('item_id').upper()
                    records.append((timestamp, user_id, action, item_id))

    # Deduplicate
    unique_records = list(set(records))

    # Group by user
    user_data = defaultdict(list)
    for r in unique_records:
        user_data[r[1]].append(r)

    features = {}
    for user_id, user_records in user_data.items():
        total_actions = len(user_records)
        unique_items = len(set(r[3] for r in user_records))

        action_counts = Counter(r[2] for r in user_records)
        # Sort by count descending, then alphabetically ascending
        sorted_actions = sorted(action_counts.items(), key=lambda x: (-x[1], x[0]))
        most_frequent_action = sorted_actions[0][0]

        features[user_id] = {
            "total_actions": total_actions,
            "unique_items": unique_items,
            "most_frequent_action": most_frequent_action
        }

    return {k: features[k] for k in sorted(features.keys())}

def test_user_features_json():
    raw_logs_path = "/home/user/raw_logs.txt"
    json_path = "/home/user/user_features.json"

    assert os.path.isfile(json_path), f"The output file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected_data = get_expected_features(raw_logs_path)

    # Check keys
    assert list(actual_data.keys()) == list(expected_data.keys()), "User IDs (keys) in the output do not match the expected sorted normalized user IDs."

    for user_id, expected_features in expected_data.items():
        actual_features = actual_data[user_id]

        assert "total_actions" in actual_features, f"Missing 'total_actions' for user {user_id}"
        assert actual_features["total_actions"] == expected_features["total_actions"], f"Incorrect 'total_actions' for user {user_id}"

        assert "unique_items" in actual_features, f"Missing 'unique_items' for user {user_id}"
        assert actual_features["unique_items"] == expected_features["unique_items"], f"Incorrect 'unique_items' for user {user_id}"

        assert "most_frequent_action" in actual_features, f"Missing 'most_frequent_action' for user {user_id}"
        assert actual_features["most_frequent_action"] == expected_features["most_frequent_action"], f"Incorrect 'most_frequent_action' for user {user_id}"