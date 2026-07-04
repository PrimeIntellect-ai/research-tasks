# test_final_state.py
import os
import json
import pytest

def test_timeline_json_exists():
    assert os.path.isfile('/home/user/timeline.json'), "The /home/user/timeline.json file is missing. Did you run the fixed aggregator script?"

def test_timeline_json_format_and_content():
    with open('/home/user/timeline.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/timeline.json does not contain valid JSON.")

    assert isinstance(data, list), "The JSON root must be an array (list)."

    expected_data = [
        {
            "timestamp": 1690000000,
            "service": "service_a",
            "message": "System started"
        },
        {
            "timestamp": 1690000010,
            "service": "service_b",
            "message": "Database connected"
        },
        {
            "timestamp": 1690000025,
            "service": "service_a",
            "message": "User logged in"
        },
        {
            "timestamp": 1690000030,
            "service": "service_b",
            "message": "Query executed"
        }
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} events, but found {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Event at index {i} is not a JSON object."

        # Check exact keys
        actual_keys = set(actual.keys())
        expected_keys = {"timestamp", "service", "message"}
        assert actual_keys == expected_keys, f"Event at index {i} has incorrect keys. Expected {expected_keys}, got {actual_keys}."

        # Check values
        assert actual["timestamp"] == expected["timestamp"], f"Event at index {i} has incorrect timestamp. Expected {expected['timestamp']}, got {actual['timestamp']}."
        assert actual["service"] == expected["service"], f"Event at index {i} has incorrect service. Expected '{expected['service']}', got '{actual['service']}'."
        assert actual["message"] == expected["message"], f"Event at index {i} has incorrect message. Expected '{expected['message']}', got '{actual['message']}'."

def test_timeline_is_sorted():
    with open('/home/user/timeline.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/timeline.json does not contain valid JSON.")

    if not isinstance(data, list):
        pytest.fail("The JSON root must be an array (list).")

    timestamps = [event.get("timestamp", 0) for event in data if isinstance(event, dict)]
    assert timestamps == sorted(timestamps), "The events in timeline.json are not sorted strictly by timestamp in ascending order."