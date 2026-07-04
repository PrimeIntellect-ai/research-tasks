# test_final_state.py

import os
import json
import pytest

OUTPUT_FILE = "/home/user/timeline_TXN-999.json"
LOG_DIR = "/home/user/logs"

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"The output file {OUTPUT_FILE} was not created."

def test_output_file_is_valid_json():
    with open(OUTPUT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The output file {OUTPUT_FILE} is not valid JSON.")

    assert isinstance(data, list), "The output JSON must be a list of events."

def test_output_timeline_contents():
    with open(OUTPUT_FILE, 'r') as f:
        data = json.load(f)

    assert len(data) == 4, f"Expected exactly 4 events in the timeline, but found {len(data)}."

    expected_event_ids = ["evt-start", "evt-2", "evt-3", "evt-4"]
    actual_event_ids = [event.get("event_id") for event in data]

    assert actual_event_ids == expected_event_ids, (
        f"Expected event order {expected_event_ids}, but got {actual_event_ids}."
    )

    # Check evt-3 timestamp normalization
    evt_3 = data[2]
    assert evt_3.get("event_id") == "evt-3"

    timestamp = evt_3.get("timestamp")
    assert timestamp in (1700000010, 1700000010.0), (
        f"The timestamp for evt-3 was not normalized correctly. "
        f"Expected 1700000010, got {timestamp}."
    )

def test_original_logs_unmodified():
    # Verify that the original log files were not modified
    evt_3_path = os.path.join(LOG_DIR, "evt-3.json")
    assert os.path.isfile(evt_3_path), f"Original log file {evt_3_path} is missing."

    with open(evt_3_path, 'r') as f:
        evt_3_data = json.load(f)

    assert evt_3_data.get("timestamp") == 1700000010000, (
        "The original log file evt-3.json was modified. You must only modify the python script."
    )