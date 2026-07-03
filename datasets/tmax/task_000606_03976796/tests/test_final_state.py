# test_final_state.py

import os
import json
import pytest
import requests

PORT = 8192
TOKEN = "AlphaTango!44"
BASE_URL = f"http://127.0.0.1:{PORT}"
LOG_FILE = "/home/user/alerts.log"

def test_poll_endpoint():
    """Test that GET /poll returns the expected JSON response."""
    try:
        response = requests.get(f"{BASE_URL}/poll", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to GET /poll: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response from /poll, got: {response.text}")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("usage") == 8492, f"Expected usage 8492, got {data.get('usage')}"

def test_alert_endpoint_unauthorized():
    """Test that POST /alert rejects requests without valid Bearer token."""
    # No auth
    try:
        response = requests.post(f"{BASE_URL}/alert", json={"test": "data"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to POST /alert: {e}")

    assert response.status_code == 401, f"Expected 401 for missing auth, got {response.status_code}"

    # Invalid auth
    headers = {"Authorization": "Bearer WrongToken"}
    response = requests.post(f"{BASE_URL}/alert", headers=headers, json={"test": "data"}, timeout=5)
    assert response.status_code == 401, f"Expected 401 for invalid auth, got {response.status_code}"

def test_alert_endpoint_authorized():
    """Test that POST /alert accepts requests with valid token and logs the payload."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {"message": "Disk space critical test"}

    try:
        response = requests.post(f"{BASE_URL}/alert", headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to POST /alert: {e}")

    assert response.status_code == 200, f"Expected 200 for valid auth, got {response.status_code}"

    # Check if log file exists and contains the payload
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} was not created"

    with open(LOG_FILE, "r") as f:
        log_content = f.read()

    # The payload might be written as a JSON string, check if the message is in the log
    assert "Disk space critical test" in log_content, f"Expected payload not found in {LOG_FILE}"