# test_final_state.py
import subprocess
import tempfile
import hmac
import hashlib
import requests
import json
import pytest

def get_elf_salt():
    try:
        with tempfile.NamedTemporaryFile() as tmp:
            subprocess.run(
                ['objcopy', '-O', 'binary', '--only-section=.secret_salt', '/app/legacy_crypto.so', tmp.name],
                check=True,
                capture_output=True
            )
            with open(tmp.name, 'rb') as f:
                salt_bytes = f.read()
                # Remove null terminators
                return salt_bytes.replace(b'\x00', b'').decode('utf-8')
    except Exception:
        # Fallback to truth value if objcopy fails
        return "L3g4cy_S@1t_88"

def test_verify_endpoint():
    # 1. Derive the key
    master_key = "M4ST3R_K3Y_2024_R0T4T10N"
    elf_salt = get_elf_salt()
    hmac_key = f"{master_key}:{elf_salt}".encode('utf-8')

    # 2. Construct valid token
    payload = "user=admin&role=superuser"
    payload_hex = payload.encode('utf-8').hex()

    valid_hmac = hmac.new(hmac_key, payload.encode('utf-8'), hashlib.sha256).hexdigest()
    valid_token = f"{payload_hex}.{valid_hmac}"

    # 3. Construct invalid token
    invalid_token = f"{payload_hex}.deadbeefdeadbeef"

    url = "http://127.0.0.1:8080/verify"
    headers = {"Content-Type": "application/json"}

    # Test valid token
    try:
        resp_valid = requests.post(url, json={"token": valid_token}, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the validation service at {url}: {e}")

    assert resp_valid.status_code == 200, f"Expected HTTP 200 for valid token, got {resp_valid.status_code}. Response: {resp_valid.text}"
    try:
        json_valid = resp_valid.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response for valid token was not valid JSON: {resp_valid.text}")

    assert json_valid.get("status") == "success", f"Expected status 'success' for valid token, got: {json_valid}"

    # Test invalid token
    try:
        resp_invalid = requests.post(url, json={"token": invalid_token}, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the validation service at {url}: {e}")

    assert resp_invalid.status_code == 401, f"Expected HTTP 401 for invalid token, got {resp_invalid.status_code}. Response: {resp_invalid.text}"
    try:
        json_invalid = resp_invalid.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response for invalid token was not valid JSON: {resp_invalid.text}")

    assert json_invalid.get("status") == "failed", f"Expected status 'failed' for invalid token, got: {json_invalid}"