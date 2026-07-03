# test_final_state.py

import os
import json
import pytest

def test_processed_data_exists():
    file_path = "/home/user/processed_data.json"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist. Did you run the Rust program?"

def test_processed_data_content():
    file_path = "/home/user/processed_data.json"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    expected_data = [
        {"sensor_id": "S1", "timestamp": 1600000000, "temperature": 23.0},
        {"sensor_id": "S1", "timestamp": 1600003600, "temperature": 23.0},
        {"sensor_id": "S1", "timestamp": 1600007200, "temperature": 24.0},
        {"sensor_id": "S1", "timestamp": 1600010800, "temperature": 24.0},
        {"sensor_id": "S1", "timestamp": 1600014400, "temperature": 25.0},
        {"sensor_id": "S2", "timestamp": 1600003600, "temperature": 10.0},
        {"sensor_id": "S2", "timestamp": 1600007200, "temperature": 10.0},
        {"sensor_id": "S2", "timestamp": 1600010800, "temperature": 12.0}
    ]

    assert isinstance(data, list), "The JSON output must be a list of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, but got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual.get("sensor_id") == expected["sensor_id"], f"Record {i}: Expected sensor_id {expected['sensor_id']}, got {actual.get('sensor_id')}"
        assert actual.get("timestamp") == expected["timestamp"], f"Record {i}: Expected timestamp {expected['timestamp']}, got {actual.get('timestamp')}"

        # Float comparison
        actual_temp = actual.get("temperature")
        assert isinstance(actual_temp, (int, float)), f"Record {i}: Temperature must be a number."
        assert abs(actual_temp - expected["temperature"]) < 1e-6, f"Record {i}: Expected temperature {expected['temperature']}, got {actual_temp}"