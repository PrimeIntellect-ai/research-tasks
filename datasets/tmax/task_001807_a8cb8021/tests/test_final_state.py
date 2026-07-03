# test_final_state.py
import hashlib
import json
import os
import re
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer sec-ops-token-992"}
EXPECTED_CSP = "default-src 'none'; frame-ancestors 'none';"

def get_expected_password():
    hash_path = '/app/leaked_hash.txt'
    with open(hash_path, 'r') as f:
        target_hash = f.read().strip()

    for i in range(10000):
        pin = f"{i:04d}"
        candidate = f"sysadmin{pin}"
        if hashlib.sha256(candidate.encode()).hexdigest() == target_hash:
            return candidate
    pytest.fail("Could not derive the expected password from the hash.")

def get_expected_logs():
    logs_path = '/app/raw_logs.json'
    with open(logs_path, 'r') as f:
        data = json.load(f)

    ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    cc_pattern = re.compile(r'\b\d{4} \d{4} \d{4} \d{4}\b')

    for event in data.get("events", []):
        msg = event.get("message", "")
        msg = ssn_pattern.sub("[REDACTED]", msg)
        msg = cc_pattern.sub("[REDACTED]", msg)
        event["message"] = msg

    return data

def test_api_auth_enforcement():
    # Test without auth header
    resp_logs = requests.get(f"{BASE_URL}/api/logs")
    assert resp_logs.status_code == 401, f"Expected 401 for /api/logs without auth, got {resp_logs.status_code}"

    resp_pwd = requests.get(f"{BASE_URL}/api/admin_password")
    assert resp_pwd.status_code == 401, f"Expected 401 for /api/admin_password without auth, got {resp_pwd.status_code}"

    # Test with invalid auth header
    bad_auth = {"Authorization": "Bearer invalid-token"}
    resp_logs_bad = requests.get(f"{BASE_URL}/api/logs", headers=bad_auth)
    assert resp_logs_bad.status_code == 401, f"Expected 401 for /api/logs with bad auth, got {resp_logs_bad.status_code}"

def test_api_logs_endpoint():
    resp = requests.get(f"{BASE_URL}/api/logs", headers=AUTH_HEADER)
    assert resp.status_code == 200, f"Expected 200 for /api/logs, got {resp.status_code}. Response: {resp.text}"

    # Check CSP header
    csp = resp.headers.get("Content-Security-Policy")
    assert csp is not None, "Missing Content-Security-Policy header on /api/logs"
    # Allow for minor whitespace differences
    assert csp.replace(" ", "") == EXPECTED_CSP.replace(" ", ""), f"Incorrect CSP header on /api/logs: {csp}"

    # Check Content-Type
    content_type = resp.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected application/json Content-Type, got {content_type}"

    # Check Payload
    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response from /api/logs is not valid JSON: {resp.text}")

    expected_data = get_expected_logs()
    assert data == expected_data, f"Logs payload does not match expected redacted logs.\nExpected: {expected_data}\nGot: {data}"

def test_api_admin_password_endpoint():
    resp = requests.get(f"{BASE_URL}/api/admin_password", headers=AUTH_HEADER)
    assert resp.status_code == 200, f"Expected 200 for /api/admin_password, got {resp.status_code}. Response: {resp.text}"

    # Check CSP header
    csp = resp.headers.get("Content-Security-Policy")
    assert csp is not None, "Missing Content-Security-Policy header on /api/admin_password"
    assert csp.replace(" ", "") == EXPECTED_CSP.replace(" ", ""), f"Incorrect CSP header on /api/admin_password: {csp}"

    # Check Payload
    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response from /api/admin_password is not valid JSON: {resp.text}")

    expected_password = get_expected_password()
    expected_data = {"cracked_password": expected_password}

    assert data == expected_data, f"Password payload does not match expected.\nExpected: {expected_data}\nGot: {data}"