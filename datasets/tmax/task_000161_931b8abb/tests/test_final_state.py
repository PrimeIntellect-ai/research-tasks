# test_final_state.py

import os
import json
import base64
import pytest

def test_ssh_audit_log():
    log_path = "/home/user/ssh_audit.log"
    assert os.path.isfile(log_path), f"The file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert "FAILED: PermitRootLogin" in lines, "Missing 'FAILED: PermitRootLogin' in ssh_audit.log"
    assert "FAILED: PasswordAuthentication" in lines, "Missing 'FAILED: PasswordAuthentication' in ssh_audit.log"

def test_vuln_keys_log():
    log_path = "/home/user/vuln_keys.log"
    assert os.path.isfile(log_path), f"The file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_vuln_key = "/home/user/audit/keys/id_rsa_weak"
    assert expected_vuln_key in lines, f"Missing '{expected_vuln_key}' in vuln_keys.log"

    # Ensure non-vulnerable keys are not included
    for not_vuln in ["/home/user/audit/keys/id_rsa_prod", "/home/user/audit/keys/id_rsa_dev"]:
        assert not_vuln not in lines, f"Non-vulnerable key '{not_vuln}' should not be in vuln_keys.log"

def test_payload_txt():
    payload_path = "/home/user/payload.txt"
    assert os.path.isfile(payload_path), f"The file {payload_path} does not exist."

    with open(payload_path, "r") as f:
        encoded = f.read().strip()

    try:
        decoded = base64.b64decode(encoded).decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to base64 decode the payload: {e}")

    try:
        data = json.loads(decoded)
    except Exception as e:
        pytest.fail(f"Failed to JSON parse the decoded payload: {e}")

    assert data.get("username") == "auditor", "Payload JSON does not have 'username' set to 'auditor'"
    assert data.get("role") == "admin", "Payload JSON does not have 'role' set to 'admin'"