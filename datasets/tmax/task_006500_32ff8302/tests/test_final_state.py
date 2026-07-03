# test_final_state.py

import os
import json
import pytest

def test_aligned_data_parquet_exists():
    """Check that aligned_data.parquet exists and has the correct Parquet magic bytes."""
    parquet_path = "/home/user/aligned_data.parquet"
    assert os.path.exists(parquet_path), f"Missing required file: {parquet_path}"
    assert os.path.isfile(parquet_path), f"Path is not a file: {parquet_path}"
    assert os.path.getsize(parquet_path) > 0, f"File {parquet_path} is empty."

    # Check Parquet magic bytes (PAR1)
    with open(parquet_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"PAR1", f"File {parquet_path} is not a valid Parquet file (missing PAR1 magic bytes)."

def test_anomalies_json_correctness():
    """Verify that anomalies.json exists, is valid JSON, and contains the correct anomalies."""
    json_path = "/home/user/anomalies.json"
    assert os.path.exists(json_path), f"Missing required file: {json_path}"

    with open(json_path, "r") as f:
        try:
            anomalies = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert isinstance(anomalies, list), "Anomalies JSON must be a list of objects."

    expected_anomalies = [
        {
            "timestamp": "2023-01-01T00:05:00Z",
            "sensor_id": "temp_A",
            "reason": "threshold_exceeded"
        },
        {
            "timestamp": "2023-01-01T00:10:00Z",
            "sensor_id": "press_B",
            "reason": "jump_exceeded"
        },
        {
            "timestamp": "2023-01-01T00:10:00Z",
            "sensor_id": "temp_A",
            "reason": "threshold_exceeded"
        }
    ]

    assert len(anomalies) == len(expected_anomalies), f"Expected {len(expected_anomalies)} anomalies, but found {len(anomalies)}."

    # Check exact match and ordering
    for i, (actual, expected) in enumerate(zip(anomalies, expected_anomalies)):
        assert actual.get("timestamp") == expected["timestamp"], f"Mismatch in timestamp at index {i}. Expected {expected['timestamp']}, got {actual.get('timestamp')}"
        assert actual.get("sensor_id") == expected["sensor_id"], f"Mismatch in sensor_id at index {i}. Expected {expected['sensor_id']}, got {actual.get('sensor_id')}"
        assert actual.get("reason") == expected["reason"], f"Mismatch in reason at index {i}. Expected {expected['reason']}, got {actual.get('reason')}"

def test_etl_log_correctness():
    """Verify that etl.log contains the exact required log message."""
    log_path = "/home/user/etl.log"
    assert os.path.exists(log_path), f"Missing required file: {log_path}"

    expected_msg = "[INFO] Pipeline finished. Anomalies detected: 3"

    with open(log_path, "r") as f:
        log_content = f.read()

    assert expected_msg in log_content, f"Expected log message '{expected_msg}' not found in {log_path}."