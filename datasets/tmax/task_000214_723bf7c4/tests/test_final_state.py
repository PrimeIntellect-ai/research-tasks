# test_final_state.py
import os
import json
import time
import urllib.request
import urllib.error
import pytest

def test_server_binary_exists():
    """Check if the compiled server binary exists and is executable."""
    binary_path = "/home/user/server_bin"
    assert os.path.isfile(binary_path), f"Server binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Server binary at {binary_path} is not executable"

def test_verification_log_exists():
    """Check if the verification log file exists."""
    log_path = "/home/user/verification.log"
    assert os.path.isfile(log_path), f"Verification log not found at {log_path}"

def test_api_valid_determinant():
    """Test that the API calculates the correct determinant for a valid 3x3 matrix."""
    # Wait to ensure rate limit window is clear
    time.sleep(1.1)

    url = "http://127.0.0.1:8080/api/determinant"
    # Matrix: 1 2 3 0 1 4 5 6 0 -> base64: MSAyIDMgMCAxIDQgNSA2IDA=
    data = json.dumps({"payload": "MSAyIDMgMCAxIDQgNSA2IDA="}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            resp_body = json.loads(response.read().decode('utf-8'))
            assert resp_body.get("determinant") == 1, f"Expected determinant 1, got {resp_body.get('determinant')}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"API request failed with status {e.code}: {e.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to server on port 8080: {e.reason}")

def test_api_invalid_shape():
    """Test that the API returns 400 for an invalid matrix size."""
    # Wait to ensure rate limit window is clear
    time.sleep(1.1)

    url = "http://127.0.0.1:8080/api/determinant"
    # Matrix: 1 2 -> base64: MSAy
    data = json.dumps({"payload": "MSAy"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected HTTP 400 Bad Request, but request succeeded")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected HTTP 400, got {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to server on port 8080: {e.reason}")

def test_api_rate_limiting():
    """Test that the API enforces the rate limit (max 2 requests per 1-second window)."""
    # Wait to ensure rate limit window is clear
    time.sleep(1.1)

    url = "http://127.0.0.1:8080/api/determinant"
    data = json.dumps({"payload": "MSAyIDMgMCAxIDQgNSA2IDA="}).encode('utf-8')

    statuses = []
    for _ in range(4):
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                statuses.append(response.status)
        except urllib.error.HTTPError as e:
            statuses.append(e.code)
        except urllib.error.URLError as e:
            pytest.fail(f"Could not connect to server on port 8080: {e.reason}")

    count_200 = statuses.count(200)
    count_429 = statuses.count(429)

    assert count_200 == 2, f"Expected exactly two 200 OK responses, got {count_200}. Statuses: {statuses}"
    assert count_429 == 2, f"Expected exactly two 429 Too Many Requests responses, got {count_429}. Statuses: {statuses}"