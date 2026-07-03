# test_final_state.py
import os
import json
import hmac
import hashlib
import base64
import pytest

def test_redacted_json():
    file_path = "/home/user/redacted.json"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} does not contain valid JSON.")

    expected_logs = [
        "User admin logged in with CC ****-****-****-3456 at 10:00 AM",
        "Payment processed for CC ****-****-****-7654 successfully",
        "Invalid login attempt by guest"
    ]

    assert "logs" in data, f"'logs' key missing in {file_path}."
    assert data["logs"] == expected_logs, f"Content of 'logs' in {file_path} does not match the expected redacted output."

def test_auditor_token():
    file_path = "/home/user/auditor_token.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    def encode_b64url(data):
        return base64.urlsafe_b64encode(data).rstrip(b'=')

    header = b'{"alg":"HS256","typ":"JWT"}'
    payload = b'{"role":"auditor"}'
    secret = b'auditor-secret-2023'

    header_b64 = encode_b64url(header)
    payload_b64 = encode_b64url(payload)
    msg = header_b64 + b"." + payload_b64

    sig = hmac.new(secret, msg, hashlib.sha256).digest()
    sig_b64 = encode_b64url(sig)

    expected_jwt = (msg + b"." + sig_b64).decode('utf-8')

    with open(file_path, 'r') as f:
        actual_jwt = f.read().strip()

    assert actual_jwt == expected_jwt, f"JWT in {file_path} does not match the expected token."

def test_csp_conf():
    file_path = "/home/user/csp.conf"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    expected_csp = 'add_header Content-Security-Policy "default-src \'self\'";'

    with open(file_path, 'r') as f:
        actual_csp = f.read().strip()

    assert actual_csp == expected_csp, f"Content of {file_path} does not match the expected CSP directive."