# test_final_state.py

import os
import re
import json
import base64
import hmac
import hashlib
import pytest

def decode_base64_url(s):
    padding = '=' * (4 - (len(s) % 4))
    return base64.urlsafe_b64decode(s + padding)

def verify_jwt(token, secret):
    parts = token.strip().split('.')
    if len(parts) != 3:
        return False, None, "Token does not have exactly 3 parts (header.payload.signature)"

    header_b64, payload_b64, signature_b64 = parts

    try:
        header = json.loads(decode_base64_url(header_b64).decode('utf-8'))
        if header.get('alg') != 'HS256':
            return False, None, f"Expected alg HS256, got {header.get('alg')}"
    except Exception as e:
        return False, None, f"Failed to parse header: {e}"

    # Verify signature
    message = f"{header_b64}.{payload_b64}".encode('utf-8')
    expected_sig = hmac.new(secret.encode('utf-8'), message, hashlib.sha256).digest()
    expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode('utf-8').rstrip('=')

    if signature_b64 != expected_sig_b64:
        return False, None, "JWT signature verification failed"

    try:
        payload = json.loads(decode_base64_url(payload_b64).decode('utf-8'))
        return True, payload, "Success"
    except Exception as e:
        return False, None, f"Failed to parse payload: {e}"

def get_expected_ips():
    auth_ips = set()
    auth_log_path = "/home/user/data/auth.log"
    if os.path.isfile(auth_log_path):
        with open(auth_log_path, "r") as f:
            for line in f:
                if "Failed login attempt" in line:
                    match = re.search(r'ip=([^\s]+)', line)
                    if match:
                        auth_ips.add(match.group(1))

    ufw_ips = set()
    ufw_log_path = "/home/user/data/ufw.log"
    if os.path.isfile(ufw_log_path):
        with open(ufw_log_path, "r") as f:
            for line in f:
                if "[UFW BLOCK]" in line and "DPT=8080" in line:
                    match = re.search(r'SRC=([^\s]+)', line)
                    if match:
                        ufw_ips.add(match.group(1))

    return sorted(list(auth_ips.intersection(ufw_ips)))

def test_audit_token_exists():
    token_path = "/home/user/audit_token.txt"
    assert os.path.isfile(token_path), f"Expected token file {token_path} does not exist."

def test_audit_token_validity_and_claims():
    token_path = "/home/user/audit_token.txt"
    secret_path = "/home/user/config/jwt.secret"

    assert os.path.isfile(token_path), f"Token file {token_path} missing."
    assert os.path.isfile(secret_path), f"Secret file {secret_path} missing."

    with open(token_path, "r") as f:
        token = f.read().strip()

    with open(secret_path, "r") as f:
        secret = f.read().strip()

    is_valid, payload, msg = verify_jwt(token, secret)
    assert is_valid, f"JWT validation failed: {msg}"

    assert payload is not None, "Payload could not be extracted from JWT"

    assert payload.get("role") == "compliance_analyst", \
        f"Expected role 'compliance_analyst', got {payload.get('role')}"

    expected_ips = get_expected_ips()
    audited_ips = payload.get("audited_ips")

    assert audited_ips is not None, "Claim 'audited_ips' is missing from JWT payload"
    assert isinstance(audited_ips, list), "'audited_ips' must be a JSON array"
    assert audited_ips == expected_ips, \
        f"Expected audited_ips to be {expected_ips}, but got {audited_ips}"