# test_final_state.py

import os
import json
import pytest

SUMMARY_PATH = "/home/user/summary.jsonl"

def test_summary_file_exists():
    assert os.path.isfile(SUMMARY_PATH), f"Output file {SUMMARY_PATH} is missing."

def test_summary_file_contents():
    with open(SUMMARY_PATH, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) == 5, f"Expected 5 lines in {SUMMARY_PATH}, found {len(lines)}."

    # Check if lines are sorted alphabetically
    assert lines == sorted(lines), f"Lines in {SUMMARY_PATH} are not sorted alphabetically."

    parsed_data = []
    for i, line in enumerate(lines):
        try:
            parsed_data.append(json.loads(line))
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {SUMMARY_PATH} is not valid JSON: {line}")

    expected_data = [
        {"sensor_id": "S1", "window_start": "2023-10-01T10:00:00Z", "avg_temperature": 22.0},
        {"sensor_id": "S1", "window_start": "2023-10-01T10:05:00Z", "avg_temperature": 25.0},
        {"sensor_id": "S1", "window_start": "2023-10-01T10:10:00Z", "avg_temperature": 28.0},
        {"sensor_id": "S2", "window_start": "2023-10-01T10:00:00Z", "avg_temperature": 16.0},
        {"sensor_id": "S2", "window_start": "2023-10-01T10:05:00Z", "avg_temperature": 18.5},
    ]

    # Sort expected data by the same implicit order to match
    # Since the parsed data might be in any order in the list, we sort both lists of dicts by sensor_id and window_start
    def sort_key(d):
        return (d.get("sensor_id", ""), d.get("window_start", ""))

    parsed_data_sorted = sorted(parsed_data, key=sort_key)
    expected_data_sorted = sorted(expected_data, key=sort_key)

    assert len(parsed_data_sorted) == len(expected_data_sorted), "Number of parsed JSON objects does not match expected."

    for i, (actual, expected) in enumerate(zip(parsed_data_sorted, expected_data_sorted)):
        assert actual.get("sensor_id") == expected["sensor_id"], f"Mismatch in sensor_id at item {i}"
        assert actual.get("window_start") == expected["window_start"], f"Mismatch in window_start at item {i}"

        actual_temp = actual.get("avg_temperature")
        assert actual_temp is not None, f"Missing avg_temperature at item {i}"
        assert abs(actual_temp - expected["avg_temperature"]) < 1e-5, \
            f"Mismatch in avg_temperature at item {i}. Expected {expected['avg_temperature']}, got {actual_temp}"