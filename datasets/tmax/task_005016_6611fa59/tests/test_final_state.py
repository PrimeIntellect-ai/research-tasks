# test_final_state.py

import pytest
import requests

def test_anomalies_endpoint():
    url = "http://127.0.0.1:8080/anomalies"
    headers = {
        "Authorization": "Bearer trace-mgr-77"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert isinstance(data, list), f"Expected response to be a JSON array, got {type(data).__name__}"

    expected_anomalies = [
        {"time_sec": 2.3, "config_id": "cfg_update_1"},
        {"time_sec": 5.7, "config_id": "cfg_update_2"},
        {"time_sec": 8.1, "config_id": "cfg_final"}
    ]

    assert len(data) == len(expected_anomalies), f"Expected {len(expected_anomalies)} anomalies, got {len(data)}"

    for i, expected in enumerate(expected_anomalies):
        actual = data[i]
        assert "time_sec" in actual, f"Missing 'time_sec' in anomaly {i}"
        assert "config_id" in actual, f"Missing 'config_id' in anomaly {i}"

        # Check time_sec with a small tolerance due to floating point representation
        assert abs(actual["time_sec"] - expected["time_sec"]) < 0.05, \
            f"Anomaly {i} time_sec mismatch: expected {expected['time_sec']}, got {actual['time_sec']}"

        assert actual["config_id"] == expected["config_id"], \
            f"Anomaly {i} config_id mismatch: expected {expected['config_id']}, got {actual['config_id']}"