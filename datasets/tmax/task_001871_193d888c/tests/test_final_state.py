# test_final_state.py
import os
import struct
import base64
import requests
import pytest
import time

SERVER_URL = "http://127.0.0.1:9090/decode"
AUTH_HEADER = {"Authorization": "Bearer sec-research-agent-2024"}

def wait_for_server():
    """Wait for the server_ready.log file to exist."""
    timeout = 10
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists("/tmp/server_ready.log"):
            with open("/tmp/server_ready.log", "r") as f:
                if "READY" in f.read():
                    return True
        time.sleep(0.5)
    return False

@pytest.fixture(scope="module", autouse=True)
def setup_server():
    assert wait_for_server(), "Server ready log not found or does not contain 'READY'."
    # Give the server a tiny bit of time to actually bind the port after writing the log
    time.sleep(1)

def test_auth_missing():
    """Test that requests without the Authorization header are rejected with 401."""
    payload_data = struct.pack('<Q', 123456789) + b'test_data'
    encoded_payload = base64.b64encode(payload_data).decode('utf-8')

    try:
        response = requests.post(SERVER_URL, json={"payload": encoded_payload}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}"

def test_auth_invalid():
    """Test that requests with an invalid Authorization header are rejected with 401."""
    payload_data = struct.pack('<Q', 123456789) + b'test_data'
    encoded_payload = base64.b64encode(payload_data).decode('utf-8')
    headers = {"Authorization": "Bearer invalid-token"}

    try:
        response = requests.post(SERVER_URL, json={"payload": encoded_payload}, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for invalid auth, got {response.status_code}"

def test_end_to_end_decode():
    """Test the end-to-end decoding process with a valid payload."""
    test_key = 9876543210987654
    payload_data = struct.pack('<Q', test_key) + b'some_encoded_blocks'
    encoded_payload = base64.b64encode(payload_data).decode('utf-8')

    try:
        response = requests.post(SERVER_URL, json={"payload": encoded_payload}, headers=AUTH_HEADER, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "decoded_key" in data, "Response JSON missing 'decoded_key'"
    assert "status" in data, "Response JSON missing 'status'"

    assert data["status"] == "success", f"Expected status 'success', got {data['status']}"
    assert data["decoded_key"] == test_key, f"Expected decoded_key {test_key}, got {data['decoded_key']}"