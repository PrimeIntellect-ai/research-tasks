# test_final_state.py

import os
import json

def test_events_bin_exists_and_correct_size():
    bin_path = "/home/user/events.bin"
    assert os.path.isfile(bin_path), f"Missing generated file: {bin_path}. Did you run profiler_dump?"
    assert os.path.getsize(bin_path) == 96, f"File {bin_path} has incorrect size. Expected 96 bytes."

def test_events_json_exists_and_correct():
    json_path = "/home/user/events.json"
    assert os.path.isfile(json_path), f"Missing file: {json_path}. Did you run the fixed parse_events.py?"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    assert isinstance(data, list), f"JSON root should be a list, found {type(data)}."
    assert len(data) == 3, f"Expected 3 events in JSON, found {len(data)}."

    expected_events = [
        {"timestamp": 1625091234, "event_type": 1, "function_name": "main"},
        {"timestamp": 1625091240, "event_type": 2, "function_name": "compute_hash"},
        {"timestamp": 1625091245, "event_type": 2, "function_name": "validate_data"}
    ]

    for i, (actual, expected) in enumerate(zip(data, expected_events)):
        assert actual.get("timestamp") == expected["timestamp"], f"Event {i} has incorrect timestamp."
        assert actual.get("event_type") == expected["event_type"], f"Event {i} has incorrect event_type."
        assert actual.get("function_name") == expected["function_name"], f"Event {i} has incorrect function_name."

def test_diff_analysis_txt_correct():
    txt_path = "/home/user/diff_analysis.txt"
    assert os.path.isfile(txt_path), f"Missing file: {txt_path}."

    with open(txt_path, 'r') as f:
        content = f.read().strip()

    assert content == "validate_data", f"Incorrect content in {txt_path}. Expected 'validate_data', got '{content}'."