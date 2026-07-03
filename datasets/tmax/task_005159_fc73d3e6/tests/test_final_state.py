# test_final_state.py

import os
import requests
import pytest
import time

API_URL = "http://127.0.0.1:9000/check_access"
LOG_FILE = "/home/user/access_audit.log"

def wait_for_service():
    for _ in range(10):
        try:
            requests.get("http://127.0.0.1:9000/")
            return
        except requests.exceptions.ConnectionError:
            pass
        try:
            requests.post(API_URL, json={})
            return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    wait_for_service()
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

def test_path_traversal():
    payload = {
        "file_path": "/etc/../shadow",
        "auth_token": "test",
        "justification": "none"
    }
    response = requests.post(API_URL, json=payload)
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    assert response.json() == {"error": "Malicious path detected"}, "Incorrect error message for path traversal"

def test_double_slash():
    payload = {
        "file_path": "/etc//shadow",
        "auth_token": "test",
        "justification": "none"
    }
    response = requests.post(API_URL, json=payload)
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    assert response.json() == {"error": "Malicious path detected"}, "Incorrect error message for double slash"

def test_integrity_failure():
    payload = {
        "file_path": "/home/user/modified.txt",
        "auth_token": "valid",
        "justification": "none"
    }
    response = requests.post(API_URL, json=payload)
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    assert response.json() == {"error": "Integrity check failed"}, "Incorrect error message for integrity failure"

def test_success_granted():
    payload = {
        "file_path": "/home/user/valid.txt",
        "auth_token": "sekret",
        "justification": "Check 123-45-6789."
    }
    response = requests.post(API_URL, json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data.get("access") == "GRANTED", "Access should be GRANTED"
    assert data.get("logged_justification") == "Check ***-**-****.", "Justification not correctly redacted"

def test_success_denied():
    payload = {
        "file_path": "/home/user/valid.txt",
        "auth_token": "wrong",
        "justification": "View 000-00-0000"
    }
    response = requests.post(API_URL, json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data.get("access") == "DENIED", "Access should be DENIED"
    assert data.get("logged_justification") == "View ***-**-****", "Justification not correctly redacted"

def test_audit_log():
    assert os.path.exists(LOG_FILE), "Audit log file was not created"
    with open(LOG_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # We expect exactly 2 lines from the successful requests
    assert len(lines) >= 2, "Audit log should contain at least 2 entries for the valid requests"

    expected_granted = "[GRANTED] - File: /home/user/valid.txt - Justification: Check ***-**-****."
    expected_denied = "[DENIED] - File: /home/user/valid.txt - Justification: View ***-**-****"

    assert expected_granted in lines, f"Expected log entry '{expected_granted}' not found"
    assert expected_denied in lines, f"Expected log entry '{expected_denied}' not found"