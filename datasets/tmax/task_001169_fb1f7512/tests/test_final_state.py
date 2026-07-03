# test_final_state.py

import os
import hashlib
import base64
import json

def test_binary_hash():
    binary_path = "/home/user/auth_verifier"
    hash_file_path = "/home/user/binary_hash.txt"

    assert os.path.isfile(binary_path), f"Binary {binary_path} is missing."
    assert os.path.isfile(hash_file_path), f"Hash file {hash_file_path} is missing."

    with open(binary_path, "rb") as f:
        expected_hash = hashlib.sha256(f.read()).hexdigest()

    with open(hash_file_path, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected hash {expected_hash}, but found {actual_hash} in {hash_file_path}"

def test_forged_token():
    token_path = "/home/user/forged_token.jwt"
    assert os.path.isfile(token_path), f"Forged token file {token_path} is missing."

    with open(token_path, "r") as f:
        token = f.read().strip()

    parts = token.split(".")
    assert len(parts) == 3, "Token must have exactly 3 parts separated by '.'"
    assert parts[2] == "", "Signature part must be empty for alg: none"

    def decode_b64url(s):
        s = s.replace("-", "+").replace("_", "/")
        padding = len(s) % 4
        if padding > 0:
            s += "=" * (4 - padding)
        return base64.b64decode(s).decode("utf-8")

    try:
        header_str = decode_b64url(parts[0])
        header = json.loads(header_str)
    except Exception as e:
        pytest.fail(f"Failed to decode or parse header: {e}")

    assert header.get("alg") == "none", "Header must contain 'alg': 'none'"

    try:
        payload_str = decode_b64url(parts[1])
        payload = json.loads(payload_str)
    except Exception as e:
        pytest.fail(f"Failed to decode or parse payload: {e}")

    assert payload.get("role") == "superadmin", "Payload must contain 'role': 'superadmin'"
    assert payload.get("sub") == "auditor", "Payload must contain 'sub': 'auditor'"

def test_audit_trail():
    log_path = "/home/user/audit_trail.log"
    assert os.path.isfile(log_path), f"Audit trail log {log_path} is missing."

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "Audit Trail Generated: Authentication Success" in log_content, "Missing authentication success message in log."
    assert "Granted Access Level: SUPERADMIN" in log_content, "Missing SUPERADMIN access level in log."
    assert "Subject: auditor" in log_content, "Missing Subject: auditor in log."