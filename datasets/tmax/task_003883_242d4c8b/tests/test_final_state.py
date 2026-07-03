# test_final_state.py

import pytest
import requests
import math

def calibrate(val):
    return (val * 1.045) + math.sin(val) * 2.1

def test_process_endpoint():
    # Construct CSV payload with Windows-1252 encoding
    csv_content = (
        "timestamp,sensor_id,raw_value\n"
        "2024-01-01T10:00:00Z,S1,10.0\n"
        "2024-01-01T10:00:03Z,S1,16.0\n"
        "2024-01-01T10:00:04Z,S1,\n"
        "2024-01-01T10:00:05Z,S1,20.0\n"
    )
    payload = csv_content.encode('windows-1252')

    try:
        response = requests.post("http://127.0.0.1:8000/process", data=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service or request timed out: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected = [
        {"timestamp": "2024-01-01T10:00:00Z", "sensor_id": "S1", "calibrated_value": round(calibrate(10.0), 3)},
        {"timestamp": "2024-01-01T10:00:01Z", "sensor_id": "S1", "calibrated_value": round(calibrate(11.0), 3)},
        {"timestamp": "2024-01-01T10:00:02Z", "sensor_id": "S1", "calibrated_value": round(calibrate(12.0), 3)},
        {"timestamp": "2024-01-01T10:00:03Z", "sensor_id": "S1", "calibrated_value": round(calibrate(13.0), 3)},
        {"timestamp": "2024-01-01T10:00:04Z", "sensor_id": "S1", "calibrated_value": round(calibrate(14.0), 3)},
        {"timestamp": "2024-01-01T10:00:05Z", "sensor_id": "S1", "calibrated_value": round(calibrate(16.0), 3)},
    ]

    assert isinstance(data, list), "Expected response to be a JSON array"
    assert len(data) == len(expected), f"Expected {len(expected)} items, got {len(data)}"

    for i, (act, exp) in enumerate(zip(data, expected)):
        assert act.get("timestamp") == exp["timestamp"], f"Item {i}: expected timestamp {exp['timestamp']}, got {act.get('timestamp')}"
        assert act.get("sensor_id") == exp["sensor_id"], f"Item {i}: expected sensor_id {exp['sensor_id']}, got {act.get('sensor_id')}"

        act_val = act.get("calibrated_value")
        assert act_val is not None, f"Item {i}: missing 'calibrated_value'"
        assert isinstance(act_val, (int, float)), f"Item {i}: 'calibrated_value' must be a number"
        assert abs(act_val - exp["calibrated_value"]) <= 0.001, f"Item {i}: expected calibrated_value ~{exp['calibrated_value']}, got {act_val}"