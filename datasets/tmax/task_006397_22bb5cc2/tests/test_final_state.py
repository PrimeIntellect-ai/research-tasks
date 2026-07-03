# test_final_state.py

import os
import json
import base64
import hmac
import hashlib
import subprocess
import re
import ipaddress
import pytest

def test_certificates():
    """Test that the certificates are correctly generated and valid."""
    ca_crt = "/home/user/certs/ca.crt"
    server_crt = "/home/user/certs/server.crt"

    assert os.path.exists(ca_crt), f"Missing Root CA certificate at {ca_crt}"
    assert os.path.exists(server_crt), f"Missing server certificate at {server_crt}"

    # Verify the certificate chain
    verify_cmd = ["openssl", "verify", "-CAfile", ca_crt, server_crt]
    res_verify = subprocess.run(verify_cmd, capture_output=True, text=True)
    assert res_verify.returncode == 0 and "OK" in res_verify.stdout, \
        f"Certificate verification failed. Output:\n{res_verify.stdout}\n{res_verify.stderr}"

    # Check the Common Name (CN) of the server certificate
    subject_cmd = ["openssl", "x509", "-in", server_crt, "-noout", "-subject"]
    res_subject = subprocess.run(subject_cmd, capture_output=True, text=True)
    assert "CN = secure.localnet" in res_subject.stdout or "CN=secure.localnet" in res_subject.stdout, \
        f"Server certificate does not have the correct Common Name (secure.localnet). Subject found: {res_subject.stdout}"

def test_jwt_token():
    """Test that the new JWT token is correctly generated and signed."""
    token_path = "/home/user/new_token.txt"
    assert os.path.exists(token_path), f"Missing token file at {token_path}"

    with open(token_path, 'r') as f:
        token = f.read().strip()

    parts = token.split('.')
    assert len(parts) == 3, "Token in new_token.txt does not appear to be a valid JWT (should have 3 parts separated by dots)."

    header_b64, payload_b64, sig_b64 = parts

    def decode_b64(data):
        # Add padding if necessary
        return base64.urlsafe_b64decode(data + '=' * (-len(data) % 4))

    try:
        header = json.loads(decode_b64(header_b64))
        payload = json.loads(decode_b64(payload_b64))
    except Exception as e:
        pytest.fail(f"Failed to decode JWT header or payload: {e}")

    assert header.get('alg') == 'HS256', f"Expected algorithm HS256, got {header.get('alg')}"

    expected_payload = {"sub": "admin", "role": "superuser", "rotated": True}
    assert payload == expected_payload, f"JWT payload does not match expected claims. Got: {payload}"

    # Verify the HMAC-SHA256 signature manually
    msg = f"{header_b64}.{payload_b64}".encode('utf-8')
    secret = b"NewSecureRotatedSecret_99!"
    expected_sig = hmac.new(secret, msg, hashlib.sha256).digest()
    expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode('utf-8').rstrip('=')

    assert sig_b64 == expected_sig_b64, "JWT signature is invalid. Ensure it was signed with the correct secret and algorithm."

def test_blocked_ips():
    """Test that the blocked_ips.txt file contains the correct IPs extracted from auth.log."""
    log_path = "/home/user/logs/auth.log"
    blocked_path = "/home/user/blocked_ips.txt"

    assert os.path.exists(blocked_path), f"Missing blocked IPs file at {blocked_path}"
    assert os.path.exists(log_path), f"Missing auth.log file at {log_path} (should not have been deleted)"

    # Derive the expected malicious IPs from the log file directly
    expected_ips = set()
    with open(log_path, 'r') as f:
        for line in f:
            match = re.search(r'IP:\s+(\S+)\s+Token:\s+(\S+)', line)
            if match:
                ip_str = match.group(1)
                token = match.group(2)
                parts = token.split('.')
                if len(parts) >= 2:
                    payload_b64 = parts[1]
                    try:
                        payload_json = base64.urlsafe_b64decode(payload_b64 + '=' * (-len(payload_b64) % 4))
                        payload = json.loads(payload_json)
                        if payload.get("malicious") is True:
                            expected_ips.add(ip_str)
                    except Exception:
                        continue

    # Sort IPs in ascending numerical order
    expected_sorted = sorted(list(expected_ips), key=lambda ip: ipaddress.ip_address(ip))

    with open(blocked_path, 'r') as f:
        actual_ips = [line.strip() for line in f if line.strip()]

    assert actual_ips == expected_sorted, \
        f"Contents of {blocked_path} do not match the expected sorted malicious IPs.\nExpected: {expected_sorted}\nGot: {actual_ips}"