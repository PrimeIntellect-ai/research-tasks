# test_final_state.py

import os
import json
import math

def test_go_file_exists():
    path = "/home/user/process_sensors.go"
    assert os.path.isfile(path), f"Expected Go source file {path} does not exist. Did you write your Go program?"

def test_output_json_exists_and_valid():
    path = "/home/user/top_sensors.json"
    assert os.path.isfile(path), f"Expected output file {path} does not exist. Did your Go program create it?"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} does not contain valid JSON."

    assert isinstance(data, list), f"Output in {path} must be a JSON array at the root."

def test_output_json_content():
    path = "/home/user/top_sensors.json"
    if not os.path.isfile(path):
        return  # skipped if file doesn't exist, handled by previous test

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return

    assert len(data) == 6, f"Expected exactly 6 records in {path} (top 2 from 3 active regions), but found {len(data)}."

    expected_records = [
        {"region": "East", "device_id": "dev5", "timestamp": 1620000180, "smoothed_temp": 21.0},
        {"region": "East", "device_id": "dev5", "timestamp": 1620000120, "smoothed_temp": 18.0},
        {"region": "North", "device_id": "dev2", "timestamp": 1620000180, "smoothed_temp": 24.0},
        {"region": "North", "device_id": "dev2", "timestamp": 1620000120, "smoothed_temp": 22.0},
        {"region": "South", "device_id": "dev4", "timestamp": 1620000180, "smoothed_temp": 27.666},
        {"region": "South", "device_id": "dev4", "timestamp": 1620000120, "smoothed_temp": 27.0}
    ]

    for i, exp in enumerate(expected_records):
        actual = data[i]

        for key in ["region", "device_id", "timestamp", "smoothed_temp"]:
            assert key in actual, f"Record at index {i} is missing the '{key}' key."

        assert actual["region"] == exp["region"], \
            f"Record at index {i} region mismatch: expected '{exp['region']}', got '{actual['region']}'."
        assert actual["device_id"] == exp["device_id"], \
            f"Record at index {i} device_id mismatch: expected '{exp['device_id']}', got '{actual['device_id']}'."
        assert actual["timestamp"] == exp["timestamp"], \
            f"Record at index {i} timestamp mismatch: expected {exp['timestamp']}, got {actual['timestamp']}."

        # Float comparison for smoothed_temp to account for rounding differences
        actual_temp = float(actual["smoothed_temp"])
        expected_temp = exp["smoothed_temp"]
        assert math.isclose(actual_temp, expected_temp, rel_tol=1e-2), \
            f"Record at index {i} smoothed_temp mismatch: expected ~{expected_temp}, got {actual_temp}."