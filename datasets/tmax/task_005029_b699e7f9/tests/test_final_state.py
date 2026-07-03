# test_final_state.py
import os
import urllib.request
import urllib.error
import base64
import json
import pytest

def test_status_file():
    """Test that the status.txt file exists and contains DONE."""
    status_file = "/home/user/status.txt"
    assert os.path.isfile(status_file), f"Status file missing: {status_file}"
    with open(status_file, "r") as f:
        content = f.read().strip()
    assert content == "DONE", f"Expected status file to contain 'DONE', got '{content}'"

def test_server_functionality():
    """Test the server decoding, config file creation, and rate limiting."""
    payload_text = "target_app=VerificationApp".encode('utf-16le')
    b64_payload = base64.b64encode(payload_text).decode('ascii')
    json_data = json.dumps({"config": b64_payload}).encode('utf-8')

    # Send 3 successful requests
    for i in range(3):
        req = urllib.request.Request("http://127.0.0.1:8080", data=json_data, method="POST")
        req.add_header('Content-Type', 'application/json')
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                assert response.status == 200, f"Request {i+1} failed with status {response.status}"
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to server or request {i+1} failed: {e}")

    # Verify config.mk was created with the correct content
    config_file = "/home/user/config.mk"
    assert os.path.isfile(config_file), f"Config file missing: {config_file}"
    with open(config_file, "r") as f:
        content = f.read().strip()
    assert content == "TARGET := VerificationApp", f"Unexpected config.mk content: {content}"

    # 4th request should be rate limited and return HTTP 429
    req = urllib.request.Request("http://127.0.0.1:8080", data=json_data, method="POST")
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            pytest.fail("4th request was not rate limited (expected HTTP 429)")
    except urllib.error.HTTPError as e:
        assert e.code == 429, f"Expected HTTP 429 Too Many Requests, got {e.code}"
    except Exception as e:
        pytest.fail(f"Unexpected error on 4th request: {e}")