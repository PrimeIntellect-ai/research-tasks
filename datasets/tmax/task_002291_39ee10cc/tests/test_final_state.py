# test_final_state.py

import os
import json
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"

def test_config_updated():
    config_path = "/app/vendored/legacy-sso-server-1.0.0/config.json"
    assert os.path.isfile(config_path), f"Config file not found at {config_path}"

    with open(config_path, "r") as f:
        data = json.load(f)

    assert "admin_password_plaintext" in data, "admin_password_plaintext missing from config.json"
    assert data["admin_password_plaintext"] == "supernova", "admin_password_plaintext value is incorrect in config.json"

def test_privilege_escalation_patched():
    try:
        response = requests.get(f"{BASE_URL}/admin", headers={"X-Internal-Debug-Bypass": "true"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert response.status_code in (401, 403), (
        f"Expected HTTP 401 or 403 for unauthorized access, but got {response.status_code}. "
        "The privilege escalation backdoor may not have been correctly patched."
    )

def test_login_and_secure_access():
    session = requests.Session()

    # Login test
    try:
        login_response = session.post(
            f"{BASE_URL}/login", 
            json={"username": "admin", "password": "supernova"},
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server for login: {e}")

    assert login_response.status_code == 200, f"Login failed. Expected HTTP 200, got {login_response.status_code}. Response: {login_response.text}"
    assert len(session.cookies) > 0, "No cookies were set by the login endpoint."

    # Secure access test
    try:
        admin_response = session.get(f"{BASE_URL}/admin", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server for admin access: {e}")

    assert admin_response.status_code == 200, f"Admin access failed with valid session. Expected HTTP 200, got {admin_response.status_code}. Response: {admin_response.text}"