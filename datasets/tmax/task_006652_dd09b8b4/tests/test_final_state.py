# test_final_state.py

import os
import json
import base64
import subprocess
import pytest

JWT_FILE = "/home/user/forged_payload.jwt"
SCRIPT_FILE = "/home/user/generate_payload.py"
KEYSTORE_FILE = "/home/user/server_keystore.p12"
KEYSTORE_PASS = "redteam123"

def b64url_decode(data):
    rem = len(data) % 4
    if rem > 0:
        data += '=' * (4 - rem)
    return base64.urlsafe_b64decode(data)

def test_files_exist():
    """Test that the required output files exist."""
    assert os.path.isfile(JWT_FILE), f"Missing required file: {JWT_FILE}"
    assert os.path.isfile(SCRIPT_FILE), f"Missing required file: {SCRIPT_FILE}"

def test_jwt_content_and_signature(tmp_path):
    """Test that the JWT has the correct header, payload, and a valid signature."""
    assert os.path.isfile(JWT_FILE), f"JWT file not found: {JWT_FILE}"

    with open(JWT_FILE, "r") as f:
        token = f.read().strip()

    parts = token.split(".")
    assert len(parts) == 3, "JWT must contain exactly 3 parts (header, payload, signature)"

    header_b64, payload_b64, sig_b64 = parts

    # Check header
    try:
        header = json.loads(b64url_decode(header_b64).decode('utf-8'))
    except Exception as e:
        pytest.fail(f"Failed to decode JWT header: {e}")

    assert header.get("alg") == "RS256", f"Expected alg RS256, got {header.get('alg')}"
    assert header.get("kid") == "internal-ca-01", f"Expected kid internal-ca-01, got {header.get('kid')}"

    # Check payload
    try:
        payload = json.loads(b64url_decode(payload_b64).decode('utf-8'))
    except Exception as e:
        pytest.fail(f"Failed to decode JWT payload: {e}")

    assert payload.get("role") == "admin", f"Expected role 'admin', got {payload.get('role')}"
    expected_username = "admin'/**/UNION/**/SELECT/**/1,2,3--"
    assert payload.get("username") == expected_username, f"Expected username {expected_username}, got {payload.get('username')}"

    # Verify signature
    pubkey_path = tmp_path / "pubkey.pem"
    try:
        # Extract public key
        cmd = f"openssl pkcs12 -in {KEYSTORE_FILE} -clcerts -nokeys -passin pass:{KEYSTORE_PASS} | openssl x509 -pubkey -noout"
        pubkey = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
        pubkey_path.write_bytes(pubkey)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to extract public key from keystore")

    sig_bytes = b64url_decode(sig_b64)
    sig_path = tmp_path / "sig.bin"
    sig_path.write_bytes(sig_bytes)

    data_path = tmp_path / "data.bin"
    data_path.write_bytes(f"{header_b64}.{payload_b64}".encode('utf-8'))

    try:
        subprocess.check_call(
            ["openssl", "dgst", "-sha256", "-verify", str(pubkey_path), "-signature", str(sig_path), str(data_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        pytest.fail("JWT signature verification failed. The token was not correctly signed with the keystore's private key.")