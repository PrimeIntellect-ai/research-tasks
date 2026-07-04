# test_final_state.py

import os
import hashlib
import requests
import urllib3
import json
import time

# Disable warnings for unverified HTTPS requests (self-signed certs)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_certificates_exist():
    """Verify that the TLS certificate and key were generated."""
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"

    assert os.path.exists(cert_path), f"Certificate not found at {cert_path}"
    assert os.path.exists(key_path), f"Private key not found at {key_path}"

def test_honeypot_service():
    """Send a malicious JWT to the honeypot and verify its response and logging."""
    url = "https://127.0.0.1:9090/auth"

    # Payload 1: An evasion JWT
    # Header: {"alg": "none"} -> eyJhbGciOiAibm9uZSJ9
    # Payload: {"role": "admin", "user": "redteam"} -> eyJyb2xlIjogImFkbWluIiwgInVzZXIiOiAicmVkdGVhbSJ9
    jwt_token = "eyJhbGciOiAibm9uZSJ9.eyJyb2xlIjogImFkbWluIiwgInVzZXIiOiAicmVkdGVhbSJ9."

    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    # Calculate expected SHA256 of the token
    expected_hash = hashlib.sha256(jwt_token.encode('utf-8')).hexdigest()

    # Send the request
    try:
        response = requests.post(url, headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the honeypot service at {url}: {e}"

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        json_data = response.json()
    except json.JSONDecodeError:
        assert False, f"Expected JSON response, got: {response.text}"

    assert json_data.get("status") == "logged", f"Expected response {{'status': 'logged'}}, got {json_data}"

    # Give the server a moment to write to the files if it does so asynchronously
    time.sleep(0.5)

    # Check security_logs.txt
    sec_log_path = "/home/user/security_logs.txt"
    assert os.path.exists(sec_log_path), f"Security log not found at {sec_log_path}"

    with open(sec_log_path, "r") as f:
        sec_logs = f.read()

    expected_log_entry = f"ALERT: Evasion attempt detected | Hash: {expected_hash} | Escaping to role: admin"
    assert expected_log_entry in sec_logs, f"Expected log entry '{expected_log_entry}' not found in {sec_log_path}. File contents:\n{sec_logs}"

    # Check privesc_audit.log
    audit_log_path = "/home/user/privesc_audit.log"
    assert os.path.exists(audit_log_path), f"Privilege escalation audit log not found at {audit_log_path}"

    with open(audit_log_path, "r") as f:
        audit_logs = f.read()

    expected_audit_entry = "SAFE: running as unprivileged user"
    assert expected_audit_entry in audit_logs, f"Expected audit entry '{expected_audit_entry}' not found in {audit_log_path}. File contents:\n{audit_logs}"