# test_final_state.py

import os
import json
import pytest

def test_dropped_log():
    log_path = "/home/user/dropped.log"
    assert os.path.exists(log_path), f"The file {log_path} does not exist."
    assert os.path.isfile(log_path), f"The path {log_path} is not a file."

    with open(log_path, "r") as f:
        lines = set(line.strip() for line in f if line.strip())

    expected_lines = {
        "Dropped sensor S1 at 2023-10-01T13:00:00Z",
        "Dropped sensor S2 at 2023-10-01T09:00:00Z"
    }

    missing = expected_lines - lines
    assert not missing, f"Missing expected lines in {log_path}: {missing}"

def test_clean_sensors_jsonl():
    jsonl_path = "/home/user/clean_sensors.jsonl"
    assert os.path.exists(jsonl_path), f"The file {jsonl_path} does not exist."
    assert os.path.isfile(jsonl_path), f"The path {jsonl_path} is not a file."

    actual_data = []
    with open(jsonl_path, "r") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                actual_data.append(obj)
            except json.JSONDecodeError:
                pytest.fail(f"Line {i} in {jsonl_path} is not valid JSON: {line}")

    expected_data = [
        {"sensor_id": "S1", "bucket": "2023-10-01T10:00:00Z", "mean_temp": 15.0, "rolling_avg": 15.0},
        {"sensor_id": "S1", "bucket": "2023-10-01T11:00:00Z", "mean_temp": 30.0, "rolling_avg": 22.5},
        {"sensor_id": "S1", "bucket": "2023-10-01T12:00:00Z", "mean_temp": 45.0, "rolling_avg": 30.0},
        {"sensor_id": "S1", "bucket": "2023-10-01T14:00:00Z", "mean_temp": 60.0, "rolling_avg": 45.0},
        {"sensor_id": "S2", "bucket": "2023-10-01T10:00:00Z", "mean_temp": 5.0, "rolling_avg": 5.0},
        {"sensor_id": "S2", "bucket": "2023-10-01T11:00:00Z", "mean_temp": 10.0, "rolling_avg": 7.5}
    ]

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records in {jsonl_path}, found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, f"Record at index {i} does not match expected.\nActual: {actual}\nExpected: {expected}"