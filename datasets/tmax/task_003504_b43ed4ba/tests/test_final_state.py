# test_final_state.py
import requests
import pytest

def test_metrics_endpoint():
    url = "http://127.0.0.1:9090/metrics"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the monitoring service at {url}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    expected_uptime = "healthy"
    expected_frames = 300
    expected_anomalies = 4

    assert data.get("uptime_status") == expected_uptime, \
        f"Expected 'uptime_status' to be '{expected_uptime}', got {data.get('uptime_status')}"
    assert data.get("processed_frames") == expected_frames, \
        f"Expected 'processed_frames' to be {expected_frames}, got {data.get('processed_frames')}"
    assert data.get("anomalies_detected") == expected_anomalies, \
        f"Expected 'anomalies_detected' to be {expected_anomalies}, got {data.get('anomalies_detected')}"