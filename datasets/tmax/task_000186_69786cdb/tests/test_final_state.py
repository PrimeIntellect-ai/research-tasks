# test_final_state.py

import os
import json
import pytest

def test_summary_jsonl_exists():
    """Test that the output file was created."""
    path = "/home/user/output/summary.jsonl"
    assert os.path.isfile(path), f"Output file {path} is missing. Did the script run and output to the correct location?"

def test_summary_jsonl_content():
    """Test that the aggregated results match the expected output."""
    path = "/home/user/output/summary.jsonl"

    expected_data = [
        {
            "window_start": "2023-10-01T10:00:00Z",
            "site": "North",
            "sensor_type": "humidity",
            "avg_value": 20.0,
            "alert_count": 1
        },
        {
            "window_start": "2023-10-01T10:00:00Z",
            "site": "North",
            "sensor_type": "temp",
            "avg_value": 50.0,
            "alert_count": 1
        },
        {
            "window_start": "2023-10-01T11:00:00Z",
            "site": "South",
            "sensor_type": "temp",
            "avg_value": 40.0,
            "alert_count": 1
        }
    ]

    actual_data = []
    with open(path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                actual_data.append(json.loads(line))
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {path} is not valid JSON: {line}")

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, but found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual.get("window_start") == expected["window_start"], f"Record {i} window_start mismatch: expected {expected['window_start']}, got {actual.get('window_start')}"
        assert actual.get("site") == expected["site"], f"Record {i} site mismatch: expected {expected['site']}, got {actual.get('site')}"
        assert actual.get("sensor_type") == expected["sensor_type"], f"Record {i} sensor_type mismatch: expected {expected['sensor_type']}, got {actual.get('sensor_type')}"

        # Check avg_value with a small tolerance for floating point issues, though it should be exact
        actual_avg = actual.get("avg_value")
        assert actual_avg is not None, f"Record {i} missing avg_value"
        assert abs(actual_avg - expected["avg_value"]) < 0.01, f"Record {i} avg_value mismatch: expected {expected['avg_value']}, got {actual_avg}"

        assert actual.get("alert_count") == expected["alert_count"], f"Record {i} alert_count mismatch: expected {expected['alert_count']}, got {actual.get('alert_count')}"