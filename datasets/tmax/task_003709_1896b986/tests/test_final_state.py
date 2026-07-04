# test_final_state.py

import os
import json
import pytest

def test_extractor_go_exists():
    assert os.path.isfile('/home/user/extractor.go'), "The Go program /home/user/extractor.go is missing."

def test_anomalies_jsonl_exists():
    assert os.path.isfile('/home/user/anomalies.jsonl'), "The output file /home/user/anomalies.jsonl is missing."

def test_anomalies_jsonl_content():
    expected_data = [
        {"sensor_id": "SENS-01", "reading_time": "2023-10-01T15:00:00Z", "temperature": 26.5},
        {"sensor_id": "SENS-02", "reading_time": "2023-10-01T14:00:00Z", "temperature": 21.0},
        {"sensor_id": "SENS-01", "reading_time": "2023-10-01T12:00:00Z", "temperature": 25.4},
        {"sensor_id": "SENS-02", "reading_time": "2023-10-01T11:00:00Z", "temperature": 22.1},
    ]

    with open('/home/user/anomalies.jsonl', 'r') as f:
        lines = f.read().strip().split('\n')

    # Filter out empty lines if any
    lines = [line for line in lines if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 lines in anomalies.jsonl, but found {len(lines)}."

    parsed_data = []
    for i, line in enumerate(lines):
        try:
            parsed = json.loads(line)
            parsed_data.append(parsed)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in anomalies.jsonl is not valid JSON: {line}")

    # Verify each line matches expected data
    for i, (actual, expected) in enumerate(zip(parsed_data, expected_data)):
        assert "sensor_id" in actual, f"Line {i+1} missing 'sensor_id' key."
        assert "reading_time" in actual, f"Line {i+1} missing 'reading_time' key."
        assert "temperature" in actual, f"Line {i+1} missing 'temperature' key."

        assert actual["sensor_id"] == expected["sensor_id"], f"Line {i+1} sensor_id mismatch: expected {expected['sensor_id']}, got {actual['sensor_id']}."
        assert actual["reading_time"] == expected["reading_time"], f"Line {i+1} reading_time mismatch: expected {expected['reading_time']}, got {actual['reading_time']}."
        assert float(actual["temperature"]) == expected["temperature"], f"Line {i+1} temperature mismatch: expected {expected['temperature']}, got {actual['temperature']}."