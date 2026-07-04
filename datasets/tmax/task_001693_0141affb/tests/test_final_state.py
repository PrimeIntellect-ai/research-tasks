# test_final_state.py

import os
import json

def test_report_file_exists():
    assert os.path.isfile('/home/user/report.json'), "The output file /home/user/report.json was not found."

def test_report_content_and_structure():
    with open('/home/user/report.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/report.json is not a valid JSON file."

    assert isinstance(data, list), "The output in report.json must be a JSON array."
    assert len(data) == 5, f"Expected exactly 5 items in report.json for Page 2, but found {len(data)}."

    expected_page_2 = [
        {"msg_id": 7, "sender": "Bob", "timestamp": "2023-10-01T10:30:00", "bytes": 250, "cumulative_bytes": 450},
        {"msg_id": 8, "sender": "Alice", "timestamp": "2023-10-01T10:35:00", "bytes": 80, "cumulative_bytes": 430},
        {"msg_id": 10, "sender": "Alice", "timestamp": "2023-10-01T10:45:00", "bytes": 120, "cumulative_bytes": 550},
        {"msg_id": 12, "sender": "Bob", "timestamp": "2023-10-01T10:55:00", "bytes": 210, "cumulative_bytes": 660},
        {"msg_id": 13, "sender": "David", "timestamp": "2023-10-01T11:00:00", "bytes": 310, "cumulative_bytes": 610}
    ]

    for i, expected_item in enumerate(expected_page_2):
        actual_item = data[i]

        # Check required keys
        expected_keys = {"msg_id", "sender", "timestamp", "bytes", "cumulative_bytes"}
        actual_keys = set(actual_item.keys())
        assert actual_keys == expected_keys, f"Item at index {i} has incorrect keys. Expected {expected_keys}, got {actual_keys}."

        # Check values
        assert actual_item["msg_id"] == expected_item["msg_id"], f"Item at index {i} has wrong msg_id. Expected {expected_item['msg_id']}, got {actual_item['msg_id']}."
        assert actual_item["sender"] == expected_item["sender"], f"Item at index {i} has wrong sender. Expected {expected_item['sender']}, got {actual_item['sender']}."
        assert actual_item["timestamp"] == expected_item["timestamp"], f"Item at index {i} has wrong timestamp. Expected {expected_item['timestamp']}, got {actual_item['timestamp']}."
        assert actual_item["bytes"] == expected_item["bytes"], f"Item at index {i} has wrong bytes. Expected {expected_item['bytes']}, got {actual_item['bytes']}."
        assert actual_item["cumulative_bytes"] == expected_item["cumulative_bytes"], f"Item at index {i} has wrong cumulative_bytes. Expected {expected_item['cumulative_bytes']}, got {actual_item['cumulative_bytes']}."