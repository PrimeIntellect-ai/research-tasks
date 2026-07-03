# test_final_state.py

import os
import stat
import subprocess
import base64
import json
import pytest

def test_legacy_monitor_permissions():
    """Verify that legacy_monitor has SUID removed and permissions set to 0755."""
    binary_path = "/home/user/bin/legacy_monitor"
    assert os.path.isfile(binary_path), f"Binary {binary_path} is missing."

    file_stat = os.stat(binary_path)
    mode = stat.S_IMODE(file_stat.st_mode)

    assert not (file_stat.st_mode & stat.S_ISUID), f"SUID bit is still set on {binary_path}."
    assert oct(mode) == '0o755', f"Permissions on {binary_path} are {oct(mode)}, expected 0o755."

def test_root_ca_certificate():
    """Verify that the self-signed certificate exists at the hardcoded path and is valid."""
    cert_path = "/home/user/.hidden_trust/root_ca.crt"
    assert os.path.isfile(cert_path), f"Certificate {cert_path} is missing."

    # Use openssl to verify it is a valid x509 certificate
    result = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-noout"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"File at {cert_path} is not a valid X.509 certificate. Error: {result.stderr.decode()}"

def test_jwt_auth_compiled_and_fixed():
    """Verify that the C++ binary is compiled and correctly rejects 'alg: none'."""
    bin_path = "/home/user/jwt_auth"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

    # Test with lowercase "none"
    result_lower = subprocess.run(
        [bin_path, '{"alg":"none"}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert "INVALID" in result_lower.stdout, "jwt_auth did not output 'INVALID' for 'alg: none'."

    # Test with uppercase "NONE"
    result_upper = subprocess.run(
        [bin_path, '{"alg":"NONE"}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert "INVALID" in result_upper.stdout, "jwt_auth did not output 'INVALID' for 'alg: NONE'."

def _decode_b64(data_str):
    """Helper to decode base64/base64url with missing padding."""
    # Convert base64url to standard base64
    data_str = data_str.replace('-', '+').replace('_', '/')
    # Add padding if necessary
    pad = len(data_str) % 4
    if pad:
        data_str += '=' * (4 - pad)
    return base64.b64decode(data_str)

def test_bad_token_txt():
    """Verify the forged JWT exists, is correctly structured, and has the right payload."""
    token_path = "/home/user/bad_token.txt"
    assert os.path.isfile(token_path), f"Token file {token_path} is missing."

    with open(token_path, 'r') as f:
        token = f.read().strip()

    parts = token.split('.')
    assert len(parts) == 3, f"Token must have exactly 3 parts separated by periods. Found {len(parts)} parts."
    assert parts[2] == "", "The signature part (third part) of the token must be empty."

    # Verify Header
    try:
        header_bytes = _decode_b64(parts[0])
        header = json.loads(header_bytes.decode('utf-8'))
    except Exception as e:
        pytest.fail(f"Failed to decode and parse token header: {e}")

    assert header.get("alg", "").lower() == "none", f"Header 'alg' is {header.get('alg')}, expected 'none'."
    assert header.get("typ") == "JWT", f"Header 'typ' is {header.get('typ')}, expected 'JWT'."

    # Verify Payload
    try:
        payload_bytes = _decode_b64(parts[1])
        payload = json.loads(payload_bytes.decode('utf-8'))
    except Exception as e:
        pytest.fail(f"Failed to decode and parse token payload: {e}")

    assert payload.get("role") == "admin", f"Payload 'role' is {payload.get('role')}, expected 'admin'."