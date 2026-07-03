# test_final_state.py
import os
import requests
import pytest
import time

PROXY_URL = "http://127.0.0.1:8080"
EXPECTED_TOKEN = "8xG2pL9"

def wait_for_service(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(url, timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

def test_status_and_load_balancing():
    """Verify /status endpoint and round-robin load balancing."""
    assert wait_for_service(f"{PROXY_URL}/status"), f"Service at {PROXY_URL}/status is not reachable"

    # Make first request
    resp1 = requests.get(f"{PROXY_URL}/status")
    assert resp1.status_code == 200, f"Expected HTTP 200, got {resp1.status_code}"
    assert resp1.json() == {"status": "ok"}, f"Expected {{'status': 'ok'}}, got {resp1.json()}"
    port1 = resp1.headers.get("X-Backend-Port")
    assert port1 in ["9001", "9002"], f"Expected X-Backend-Port to be 9001 or 9002, got {port1}"

    # Make second request
    resp2 = requests.get(f"{PROXY_URL}/status")
    assert resp2.status_code == 200, f"Expected HTTP 200, got {resp2.status_code}"
    assert resp2.json() == {"status": "ok"}
    port2 = resp2.headers.get("X-Backend-Port")
    assert port2 in ["9001", "9002"], f"Expected X-Backend-Port to be 9001 or 9002, got {port2}"

    # Check load balancing
    assert port1 != port2, f"Load balancing failed: both requests hit port {port1}. Expected round-robin between 9001 and 9002."

def test_users_unauthorized():
    """Verify /users endpoint without token returns 401."""
    resp = requests.get(f"{PROXY_URL}/users")
    assert resp.status_code == 401, f"Expected HTTP 401 Unauthorized for missing token, got {resp.status_code}"

def test_users_authorized():
    """Verify /users endpoint with correct token returns 200 and user list."""
    headers = {"X-Admin-Token": EXPECTED_TOKEN}
    resp = requests.get(f"{PROXY_URL}/users", headers=headers)
    assert resp.status_code == 200, f"Expected HTTP 200 for valid token, got {resp.status_code}"
    expected_data = {"users": ["alice", "bob", "charlie"]}
    assert resp.json() == expected_data, f"Expected {expected_data}, got {resp.json()}"

def test_proxy_access_log():
    """Verify that the Nginx access log exists and contains entries."""
    log_path = "/home/user/proxy_access.log"
    assert os.path.isfile(log_path), f"Access log not found at {log_path}"
    assert os.path.getsize(log_path) > 0, f"Access log at {log_path} is empty"