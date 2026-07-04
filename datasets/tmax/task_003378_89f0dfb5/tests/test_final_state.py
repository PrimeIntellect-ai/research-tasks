# test_final_state.py

import os
import threading
import requests
import pytest

def test_anomaly_user_file():
    """Verify that the anomaly user ID is correctly identified and written to the file."""
    path = "/home/user/anomaly_user.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "4044", f"Expected anomaly user ID '4044', but got '{content}'."

def test_go_service_auth_missing():
    """Verify that the Go service rejects requests without authentication."""
    url = "http://127.0.0.1:9000/ingest"
    payload = {"user_id": 1, "payload": "SGVsbG8_V29ybGQ="}
    try:
        response = requests.post(url, json=payload, timeout=2)
        assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}."
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service: {e}")

def test_go_service_auth_invalid():
    """Verify that the Go service rejects requests with invalid authentication."""
    url = "http://127.0.0.1:9000/ingest"
    payload = {"user_id": 1, "payload": "SGVsbG8_V29ybGQ="}
    headers = {"Authorization": "Bearer wrong_token"}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
        assert response.status_code == 401, f"Expected HTTP 401 for invalid auth, got {response.status_code}."
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service: {e}")

def test_go_service_concurrency_and_payload():
    """Verify that the Go service handles concurrent requests and correctly decodes Base64URL payloads."""
    url = "http://127.0.0.1:9000/ingest"
    payload = {"user_id": 1, "payload": "SGVsbG8_V29ybGQ="}
    headers = {"Authorization": "Bearer 8675309"}

    errors = []

    def make_request():
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            if response.status_code != 200:
                errors.append(f"Expected HTTP 200, got {response.status_code}: {response.text}")
        except Exception as e:
            errors.append(str(e))

    # Send multiple concurrent requests to test for race conditions
    threads = []
    for _ in range(50):
        t = threading.Thread(target=make_request)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert not errors, f"Errors occurred during concurrent requests: {errors[:5]}"