# test_final_state.py

import os
import json
import pytest

def test_merged_timeline_exists():
    out_file = "/home/user/build/merged_timeline.json"
    assert os.path.isfile(out_file), f"The output file {out_file} was not created. Did you run the ingest.py script?"

def test_merged_timeline_valid_json():
    out_file = "/home/user/build/merged_timeline.json"
    assert os.path.isfile(out_file), f"The output file {out_file} is missing."

    with open(out_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {out_file} does not contain valid JSON.")

    assert isinstance(data, list), f"The JSON in {out_file} should be a list of objects."

def test_merged_timeline_sorted_correctly():
    out_file = "/home/user/build/merged_timeline.json"
    assert os.path.isfile(out_file), f"The output file {out_file} is missing."

    with open(out_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {out_file} does not contain valid JSON.")

    expected_messages = [
        "Initializing service C workers",
        "Started processing batch A",
        "Received data from upstream",
        "Completed batch A",
        "Heartbeat ping successful",
        "Sent data downstream",
        "Shutting down workers"
    ]

    actual_messages = [event.get("message") for event in data if isinstance(event, dict)]

    assert actual_messages == expected_messages, (
        "The timeline is not sorted correctly or is missing events. "
        f"Expected messages in order: {expected_messages}, but got: {actual_messages}"
    )

def test_merged_timeline_structure():
    out_file = "/home/user/build/merged_timeline.json"
    assert os.path.isfile(out_file), f"The output file {out_file} is missing."

    with open(out_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {out_file} does not contain valid JSON.")

    for i, event in enumerate(data):
        assert isinstance(event, dict), f"Event at index {i} is not a JSON object."
        assert "service" in event, f"Event at index {i} is missing the 'service' key."
        assert "timestamp" in event, f"Event at index {i} is missing the 'timestamp' key."
        assert "message" in event, f"Event at index {i} is missing the 'message' key."