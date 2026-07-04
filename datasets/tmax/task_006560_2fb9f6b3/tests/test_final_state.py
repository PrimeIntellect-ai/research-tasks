# test_final_state.py

import os
import json
import pytest

OUTPUT_FILE = "/home/user/output.jsonl"
STATS_FILE = "/home/user/stats.json"

def test_stats_file_exists_and_correct():
    """Test that stats.json exists and contains the correct pipeline statistics."""
    assert os.path.exists(STATS_FILE), f"Stats file {STATS_FILE} is missing."
    assert os.path.isfile(STATS_FILE), f"{STATS_FILE} is not a file."

    with open(STATS_FILE, "r") as f:
        try:
            stats = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{STATS_FILE} does not contain valid JSON.")

    expected_stats = {
        "total_read": 5,
        "dropped_invalid": 1,
        "dropped_duplicates": 1,
        "total_output": 3
    }

    for key, expected_value in expected_stats.items():
        assert key in stats, f"Key '{key}' missing in {STATS_FILE}."
        assert stats[key] == expected_value, f"Expected {key} to be {expected_value}, got {stats[key]}."

def test_output_file_exists_and_correct():
    """Test that output.jsonl exists, has 3 lines, and contains correct transformed data."""
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} is missing."
    assert os.path.isfile(OUTPUT_FILE), f"{OUTPUT_FILE} is not a file."

    with open(OUTPUT_FILE, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 3, f"Expected exactly 3 lines in {OUTPUT_FILE}, but got {len(lines)}."

    expected_data = [
        {"event_id": "e1", "device_model": "ModelA", "temperature_c": 0},
        {"event_id": "e3", "device_model": "ModelC-Pro", "temperature_c": 37},
        {"event_id": "e4", "device_model": "Legacy", "temperature_c": -40}
    ]

    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {OUTPUT_FILE} is not valid JSON.")

        expected = expected_data[i]

        assert record.get("event_id") == expected["event_id"], f"Line {i+1}: expected event_id '{expected['event_id']}', got '{record.get('event_id')}'."
        assert record.get("device_model") == expected["device_model"], f"Line {i+1}: expected device_model '{expected['device_model']}', got '{record.get('device_model')}'."

        assert "user_agent" not in record, f"Line {i+1}: 'user_agent' field should be removed."
        assert "sensor_data" in record, f"Line {i+1}: 'sensor_data' object is missing."

        sensor_data = record["sensor_data"]
        assert "temperature_f" not in sensor_data, f"Line {i+1}: 'temperature_f' field should be removed from sensor_data."
        assert "temperature_c" in sensor_data, f"Line {i+1}: 'temperature_c' field missing in sensor_data."
        assert sensor_data["temperature_c"] == expected["temperature_c"], f"Line {i+1}: expected temperature_c {expected['temperature_c']}, got {sensor_data['temperature_c']}."

        assert "timestamp" in record, f"Line {i+1}: 'timestamp' field is missing."
        assert record["timestamp"] != "", f"Line {i+1}: 'timestamp' field is empty."