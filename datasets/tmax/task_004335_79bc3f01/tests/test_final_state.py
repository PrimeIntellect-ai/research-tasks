# test_final_state.py

import os
import re
import pytest
import requests
import urllib3

# Suppress insecure request warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SERVER_URL = "https://127.0.0.1:8443/auth"
CORRECT_TOKEN = "TrUSt_N0_1_XyZ99"
WRONG_TOKEN = "wrong_token"
LOG_FILE = "/home/user/auth_audit.log"

def test_certificates_exist():
    """Verify that the generated certificate and key files exist."""
    cert_path = "/home/user/server.crt"
    key_path = "/home/user/server.key"

    assert os.path.exists(cert_path), f"Certificate file missing: {cert_path}"
    assert os.path.exists(key_path), f"Private key file missing: {key_path}"

def test_auth_endpoint_success():
    """Test the HTTPS server with the correct token."""
    try:
        response = requests.post(
            SERVER_URL,
            json={"token": CORRECT_TOKEN},
            verify=False,
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTPS server at {SERVER_URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for correct token, got {response.status_code}"

    try:
        json_data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert json_data.get("status") == "success", f"Expected status 'success', got {json_data.get('status')}"

def test_auth_endpoint_forbidden():
    """Test the HTTPS server with an incorrect token."""
    try:
        response = requests.post(
            SERVER_URL,
            json={"token": WRONG_TOKEN},
            verify=False,
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTPS server at {SERVER_URL}: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 for incorrect token, got {response.status_code}"

    try:
        json_data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert json_data.get("status") == "forbidden", f"Expected status 'forbidden', got {json_data.get('status')}"

def test_auth_audit_log():
    """Verify that the audit log contains the required ALLOW and DENY entries."""
    assert os.path.exists(LOG_FILE), f"Audit log file missing: {LOG_FILE}"

    with open(LOG_FILE, "r") as f:
        log_content = f.read()

    allow_pattern = r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] 127\.0\.0\.1 - Action: ALLOW"
    deny_pattern = r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] 127\.0\.0\.1 - Action: DENY"

    assert re.search(allow_pattern, log_content), "Audit log is missing the required ALLOW entry format."
    assert re.search(deny_pattern, log_content), "Audit log is missing the required DENY entry format."