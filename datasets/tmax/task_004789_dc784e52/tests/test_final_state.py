# test_final_state.py
import requests
import time
import pytest

def test_service_running_and_detects_anomaly():
    base_url = "http://127.0.0.1:9000"

    # Wait for the service to be up
    max_retries = 5
    for i in range(max_retries):
        try:
            # Just check if we can connect
            requests.get(f"{base_url}/anomalies", timeout=2)
            break
        except requests.exceptions.ConnectionError:
            if i == max_retries - 1:
                pytest.fail("Service is not running on 127.0.0.1:9000")
            time.sleep(1)

    payload = [
        {"service": "A", "timestamp": "2023-10-01T23:58:00Z", "latency_ms": 10},
        {"service": "A", "timestamp": "2023-10-01T23:59:00Z", "latency_ms": 12},
        {"service": "A", "timestamp": "2023-10-02T00:01:00Z", "latency_ms": 100}
    ]

    ingest_resp = requests.post(f"{base_url}/ingest", json=payload, timeout=5)
    assert ingest_resp.status_code in (200, 201, 202, 204), f"Failed to ingest data, status code: {ingest_resp.status_code}, response: {ingest_resp.text}"

    anomalies_resp = requests.get(f"{base_url}/anomalies", timeout=5)
    assert anomalies_resp.status_code == 200, f"Failed to get anomalies, status code: {anomalies_resp.status_code}, response: {anomalies_resp.text}"

    try:
        anomalies = anomalies_resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {anomalies_resp.text}")

    assert isinstance(anomalies, list), f"Expected anomalies to be a JSON array, got {type(anomalies)}"

    anomaly_timestamps = [a.get("timestamp") for a in anomalies if isinstance(a, dict)]
    assert "2023-10-02T00:01:00Z" in anomaly_timestamps, (
        f"Expected anomaly at '2023-10-02T00:01:00Z' not found in anomalies list. "
        f"Found timestamps: {anomaly_timestamps}"
    )