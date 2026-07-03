# test_final_state.py
import os
import base64
import pytest

def test_vuln_path():
    path = "/home/user/vuln_path.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip()
    assert content == "/home/user/system_scripts/process_data.sh", f"Incorrect content in {path}. Expected '/home/user/system_scripts/process_data.sh'."

def test_audit_evidence():
    path = "/home/user/audit_evidence.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip()
    assert content == "AUDIT_COMPLETE", f"Incorrect content in {path}. Expected 'AUDIT_COMPLETE'."

def test_used_payload():
    path = "/home/user/used_payload.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        decoded_bytes = base64.b64decode(content)
        decoded = decoded_bytes.decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to decode base64 from {path}: {e}")

    assert "AUDIT_COMPLETE" in decoded, f"The decoded payload does not contain 'AUDIT_COMPLETE'. Payload was: {decoded}"
    assert "/home/user/audit_evidence.txt" in decoded, f"The decoded payload does not contain the target file path. Payload was: {decoded}"