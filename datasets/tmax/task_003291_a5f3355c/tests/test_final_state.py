# test_final_state.py
import os
import time
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"

def test_executable_exists():
    path = "/home/user/server_secure"
    assert os.path.exists(path), f"Missing executable: {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_open_redirect_malicious():
    try:
        response = requests.get(f"{BASE_URL}/login?next=http://attacker.com/steal", allow_redirects=False, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to server failed: {e}")

    assert response.status_code == 302, f"Expected status 302 for malicious redirect, got {response.status_code}. Response body: {response.text}"
    location = response.headers.get("Location")
    assert location == "/home", f"Expected Location header to be '/home', got '{location}'"

def test_open_redirect_safe():
    try:
        response = requests.get(f"{BASE_URL}/login?next=/profile", allow_redirects=False, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to server failed: {e}")

    assert response.status_code == 302, f"Expected status 302 for safe redirect, got {response.status_code}. Response body: {response.text}"
    location = response.headers.get("Location")
    assert location == "/profile", f"Expected Location header to be '/profile', got '{location}'"

def test_auth_and_logging():
    log_path = "/home/user/server.log"

    # Send authenticated request
    headers = {
        "Cookie": "dev_override=OmegaProtocol99; session_id=12345ABC;"
    }

    try:
        response = requests.get(f"{BASE_URL}/admin", headers=headers, allow_redirects=False, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to server failed: {e}")

    assert response.status_code == 200, f"Expected status 200 for authenticated request, got {response.status_code}. Response body: {response.text}"

    # Wait briefly to ensure log is flushed to disk
    time.sleep(0.5)

    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        log_content = f.read()

    assert "OmegaProtocol99" not in log_content, "Log file leaked the sensitive dev_override token 'OmegaProtocol99'."
    assert "12345ABC" not in log_content, "Log file leaked the sensitive session_id '12345ABC'."
    assert "dev_override=[REDACTED]" in log_content, "Log file does not show 'dev_override=[REDACTED]'."
    assert "session_id=[REDACTED]" in log_content, "Log file does not show 'session_id=[REDACTED]'."