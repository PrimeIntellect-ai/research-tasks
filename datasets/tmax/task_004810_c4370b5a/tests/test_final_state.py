# test_final_state.py

import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8080"
ENDPOINT = f"{BASE_URL}/policy-check"
VALID_TOKEN = "AUTH-9942X"

def wait_for_service():
    """Wait for the service to be up and running."""
    for _ in range(10):
        try:
            requests.get(BASE_URL, timeout=1)
            return
        except requests.exceptions.RequestException:
            pass
        # It's a POST only endpoint, so maybe GET fails with 405 or 404, but connection succeeds.
        try:
            requests.post(ENDPOINT, json={}, timeout=1)
            return
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)

@pytest.fixture(scope="module", autouse=True)
def setup():
    wait_for_service()

def test_missing_token():
    payload = {"user": "alice", "script_name": "deploy.sh"}
    response = requests.post(ENDPOINT, json=payload, timeout=2)
    assert response.status_code == 401, f"Expected HTTP 401 for missing token, got {response.status_code}. Response: {response.text}"

def test_incorrect_token():
    headers = {"Authorization": "Bearer WRONG-TOKEN"}
    payload = {"user": "alice", "script_name": "deploy.sh"}
    response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=2)
    assert response.status_code == 401, f"Expected HTTP 401 for incorrect token, got {response.status_code}. Response: {response.text}"

def test_valid_request_allow():
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
    payload = {"user": "alice", "script_name": "deploy.sh"}
    response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=2)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("status") == "allow", f"Expected status 'allow', got {data}"

def test_privilege_escalation_attempt():
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
    payload = {"user": "mallory", "script_name": "deploy.sh"}
    response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=2)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("status") == "deny", f"Expected status 'deny', got {data}"
    assert data.get("reason") == "escalation_attempt", f"Expected reason 'escalation_attempt', got {data}"

def test_checksum_mismatch():
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
    payload = {"user": "alice", "script_name": "backdoor.sh"}
    response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=2)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("status") == "deny", f"Expected status 'deny', got {data}"
    assert data.get("reason") == "checksum_mismatch", f"Expected reason 'checksum_mismatch', got {data}"

def test_missing_file():
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
    payload = {"user": "alice", "script_name": "nonexistent.sh"}
    response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=2)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("status") == "deny", f"Expected status 'deny', got {data}"
    assert data.get("reason") == "checksum_mismatch", f"Expected reason 'checksum_mismatch', got {data}"