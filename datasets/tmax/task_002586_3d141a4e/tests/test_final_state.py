# test_final_state.py

import pytest
import requests
import time

URL = "http://127.0.0.1:8080/process"
TOKEN = "tr0ub4d0ur&3"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

@pytest.fixture(scope="session", autouse=True)
def wait_for_service():
    """Wait for the service to be available before running tests."""
    max_retries = 10
    for _ in range(max_retries):
        try:
            # Just test if the port is open and responding
            requests.get("http://127.0.0.1:8080/", timeout=1)
            return
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
        except requests.exceptions.Timeout:
            pass
    pytest.fail("Service is not listening on 127.0.0.1:8080 after waiting.")

def test_valid_payload():
    """Test that a valid payload (< 256 bytes) is processed correctly."""
    payload = b"A" * 100
    try:
        response = requests.post(URL, headers=HEADERS, data=payload, timeout=2)
        assert response.status_code == 200, f"Expected 200 OK for valid payload, got {response.status_code}. Response: {response.text}"
        assert len(response.content) == 100, f"Expected response length 100, got {len(response.content)}"
        assert response.content == payload, "Response content does not match the input payload."
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")

def test_buffer_overflow_fix():
    """Test that an oversized payload (> 256 bytes) does not crash the service and is truncated."""
    payload = b"B" * 500
    try:
        response = requests.post(URL, headers=HEADERS, data=payload, timeout=2)
        assert response.status_code == 200, f"Expected 200 OK for oversized payload (should be truncated), got {response.status_code}. Response: {response.text}"
        assert len(response.content) == 256, f"Expected truncated payload of exactly 256 bytes, got {len(response.content)}"
        assert response.content == b"B" * 256, "Response content should be the truncated input (first 256 bytes)."
    except requests.exceptions.ConnectionError:
        pytest.fail("Service crashed (ConnectionError) when sending oversized payload! The buffer overflow vulnerability is not fixed.")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")

def test_authentication():
    """Test that the service enforces authentication using the correct token."""
    payload = b"C" * 50
    bad_headers = {"Authorization": "Bearer invalid_token_123"}
    try:
        response = requests.post(URL, headers=bad_headers, data=payload, timeout=2)
        assert response.status_code in [401, 403], f"Expected 401 Unauthorized or 403 Forbidden for invalid token, got {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")

def test_missing_authentication():
    """Test that the service enforces authentication when the header is missing."""
    payload = b"D" * 50
    try:
        response = requests.post(URL, data=payload, timeout=2)
        assert response.status_code in [401, 403], f"Expected 401 Unauthorized or 403 Forbidden for missing auth header, got {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")