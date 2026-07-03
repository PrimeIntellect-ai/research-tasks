# test_final_state.py

import os
import socket
import time
import hashlib
import requests
import pytest

def test_pyjwt_fixed():
    """Verify that the tampered PyJWT HMAC verification has been fixed."""
    algorithms_file = "/app/PyJWT-2.8.0/jwt/algorithms.py"
    assert os.path.isfile(algorithms_file), f"File {algorithms_file} is missing."
    with open(algorithms_file, "r") as f:
        content = f.read()
    assert "return False # TAMPERED" not in content, "The PyJWT library still contains the tampered code."
    assert "hmac.compare_digest" in content, "The PyJWT library does not contain the correct hmac.compare_digest fix."

def test_http_service_token_and_validate():
    """Verify the HTTP service generates and validates tokens correctly."""
    url_token = "http://127.0.0.1:8080/token"
    url_validate = "http://127.0.0.1:8080/validate"

    # Test token generation
    try:
        resp = requests.post(url_token, json={"user": "compliance_auditor"}, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {url_token}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK from /token, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Expected JSON response from /token, got: {resp.text}")

    assert "token" in data, f"Response from /token does not contain 'token' key. Got: {data}"
    token = data["token"]

    # Test token validation
    try:
        resp2 = requests.post(url_validate, json={"token": token}, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {url_validate}: {e}")

    assert resp2.status_code == 200, f"Expected 200 OK from /validate, got {resp2.status_code}. Response: {resp2.text}"

    try:
        data2 = resp2.json()
    except ValueError:
        pytest.fail(f"Expected JSON response from /validate, got: {resp2.text}")

    assert data2.get("valid") is True, f"Expected 'valid': true in response, got: {data2}"
    assert data2.get("user") == "compliance_auditor", f"Expected 'user': 'compliance_auditor' in response, got: {data2}"

def test_http_service_invalid_token():
    """Verify the HTTP service rejects invalid tokens with a 401 status."""
    url_validate = "http://127.0.0.1:8080/validate"
    try:
        resp = requests.post(url_validate, json={"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.token"}, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {url_validate}: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized from /validate for invalid token, got {resp.status_code}. Response: {resp.text}"

def test_tcp_service_audit_log():
    """Verify the TCP service correctly hashes messages and appends to the audit log."""
    message = "SYSTEM_STARTUP_EVENT"
    expected_hash = hashlib.sha256(message.encode()).hexdigest()
    expected_log_entry = f"[{expected_hash}] {message}\n"

    # Send message to TCP service
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("127.0.0.1", 8081))
        s.sendall((message + "\n").encode())
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to connect and send data to TCP service on port 8081: {e}")

    # Wait briefly for log to be written
    time.sleep(0.5)

    log_file = "/home/user/audit.log"
    assert os.path.isfile(log_file), f"Audit log file {log_file} does not exist. Ensure the TCP service creates it."

    with open(log_file, "r") as f:
        content = f.read()

    assert expected_log_entry in content, f"Expected log entry '{expected_log_entry.strip()}' not found in {log_file}. Content was: {content}"