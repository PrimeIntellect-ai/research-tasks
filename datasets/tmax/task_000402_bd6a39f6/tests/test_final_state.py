# test_final_state.py

import os
import time
import requests
import uuid

def test_unauthorized_request():
    """Verify that the API rejects unauthorized requests."""
    url = "http://127.0.0.1:8080/telemetry"
    headers = {
        "Authorization": "Bearer invalid-token",
        "Content-Type": "application/json"
    }
    payload = {"device_id": "test-device", "metric": 10.0}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        raise AssertionError(f"Failed to connect to the ingest-api on 127.0.0.1:8080: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}. Response: {response.text}"

def test_end_to_end_telemetry_pipeline():
    """Verify the full pipeline: API -> Redis -> Worker -> Log file."""
    url = "http://127.0.0.1:8080/telemetry"
    headers = {
        "Authorization": "Bearer rel-mgr-token-992",
        "Content-Type": "application/json"
    }

    # Generate a unique device ID to ensure we are not reading old logs
    unique_id = f"sensor-{uuid.uuid4().hex[:8]}"
    metric_val = 42.5
    payload = {"device_id": unique_id, "metric": metric_val}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        raise AssertionError(f"Failed to connect to the ingest-api on 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
        assert data.get("status") == "queued", f"Expected response JSON {{'status': 'queued'}}, got {data}"
    except ValueError:
        raise AssertionError(f"Response was not valid JSON: {response.text}")

    # Wait for the worker to process the queue
    log_file_path = "/home/user/app/processed_telemetry.log"
    expected_log_line = f"DEVICE:{unique_id},METRIC:{metric_val}"

    found = False
    for _ in range(20):
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as f:
                content = f.read()
                if expected_log_line in content:
                    found = True
                    break
        time.sleep(0.2)

    if not found:
        if not os.path.exists(log_file_path):
            raise AssertionError(f"Log file {log_file_path} was not created by the worker.")
        else:
            with open(log_file_path, "r") as f:
                content = f.read()
            raise AssertionError(f"Expected to find '{expected_log_line}' in {log_file_path}, but it was not there. Current content:\n{content}")