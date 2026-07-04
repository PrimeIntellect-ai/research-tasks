# test_final_state.py

import os
import subprocess
import requests
import pytest
import hmac
import hashlib
import base64

GATEWAY_URL = "http://127.0.0.1:8080"
AUTH_URL = "http://127.0.0.1:8081"

def test_forge_go_output():
    """Test that /home/user/forge.go generates the correct forged XOR token."""
    forge_path = "/home/user/forge.go"
    assert os.path.isfile(forge_path), f"Forge program missing: {forge_path}"

    try:
        result = subprocess.run(
            ["go", "run", forge_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"go run {forge_path} failed with exit code {e.returncode}. stderr: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail(f"go run {forge_path} timed out.")

    output = result.stdout.strip()

    # Compute expected XOR token
    payload = b"role=admin"
    xor_key = 0x42
    xored = bytes(b ^ xor_key for b in payload)
    expected_token = base64.b64encode(xored).decode('utf-8')

    assert output == expected_token, f"Forge program output '{output}' does not match expected '{expected_token}'"

def test_gateway_csp_header():
    """Test that the API Gateway includes the correct CSP header."""
    try:
        response = requests.get(f"{GATEWAY_URL}/", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API Gateway at {GATEWAY_URL}/: {e}")

    csp_header = response.headers.get("Content-Security-Policy")
    assert csp_header is not None, "Content-Security-Policy header is missing from the gateway response."
    assert csp_header == "default-src 'self'", f"Incorrect CSP header value: {csp_header}"

def test_gateway_rejects_old_token():
    """Test that the API Gateway rejects the old XOR token."""
    payload = b"role=admin"
    xor_key = 0x42
    xored = bytes(b ^ xor_key for b in payload)
    old_token = base64.b64encode(xored).decode('utf-8')

    headers = {"Authorization": f"Bearer {old_token}"}

    try:
        response = requests.get(f"{GATEWAY_URL}/admin", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API Gateway at {GATEWAY_URL}/admin: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for old token, got {response.status_code}"

def test_gateway_accepts_new_token():
    """Test that the API Gateway accepts the new HMAC-SHA256 token."""
    payload = b"role=admin"
    b64_payload = base64.b64encode(payload)
    secret_key = b"super_secret_hmac_key_123"

    hmac_digest = hmac.new(secret_key, b64_payload, hashlib.sha256).hexdigest()
    new_token = f"{b64_payload.decode('utf-8')}.{hmac_digest}"

    headers = {"Authorization": f"Bearer {new_token}"}

    try:
        response = requests.get(f"{GATEWAY_URL}/admin", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API Gateway at {GATEWAY_URL}/admin: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for valid HMAC token, got {response.status_code}. Response: {response.text}"