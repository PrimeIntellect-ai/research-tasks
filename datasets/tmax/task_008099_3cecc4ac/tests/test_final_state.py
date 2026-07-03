# test_final_state.py

import os
import json
import pytest

OUTPUT_PATH = "/home/user/flagged_events.json"

def test_flagged_events_file_exists():
    """Test that the output JSON file was created at the correct path."""
    assert os.path.isfile(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH}. Did your Rust program run and create it?"

def test_flagged_events_content():
    """Test that the output JSON file contains the correct flagged events in the correct order."""
    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {OUTPUT_PATH} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON root must be an array (list)."

    assert len(data) == 2, f"Expected exactly 2 flagged events, but found {len(data)}."

    expected_events = [
        {"event_id": 16, "user_id": "u1", "role_assumed": "manager"},
        {"event_id": 4, "user_id": "u1", "role_assumed": "admin"}
    ]

    for i, expected in enumerate(expected_events):
        actual = data[i]
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."

        # Check required fields
        for key in expected:
            assert key in actual, f"Missing key '{key}' in item at index {i}."
            assert actual[key] == expected[key], f"Expected {key} to be {expected[key]} at index {i}, but got {actual[key]}."