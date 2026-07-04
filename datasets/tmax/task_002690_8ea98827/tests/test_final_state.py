# test_final_state.py
import os
import stat
import base64
import hmac
import hashlib
import json
import requests
import pytest

def encode_base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def create_jwt(header: dict, payload: dict, secret: str = None) -> str:
    header_enc = encode_base64url(json.dumps(header).encode('utf-8'))
    payload_enc = encode_base64url(json.dumps(payload).encode('utf-8'))
    message = f"{header_enc}.{payload_enc}"

    if secret:
        sig = hmac.new(secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
        sig_enc = encode_base64url(sig)
        return f"{message}.{sig_enc}"
    else:
        return f"{message}."

@pytest.fixture
def valid_jwt():
    return create_jwt({"alg": "HS256", "typ": "JWT"}, {"user": "admin"}, "proxy-secret-2024")

@pytest.fixture
def none_jwt():
    return create_jwt({"alg": "none", "typ": "JWT"}, {"user": "admin"})

@pytest.fixture
def none_upper_jwt():
    return create_jwt({"alg": "NONE", "typ": "JWT"}, {"user": "admin"})

def test_valid_jwt_forwarding(valid_jwt):
    headers = {"Authorization": f"Bearer {valid_jwt}"}
    try:
        response = requests.get("http://127.0.0.1:8080/data", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the proxy: {e}")

    assert response.status_code == 200, f"Expected 200 OK for valid JWT, got {response.status_code}"

def test_alg_none_jwt_rejected(none_jwt):
    headers = {"Authorization": f"Bearer {none_jwt}"}
    try:
        response = requests.get("http://127.0.0.1:8080/data", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the proxy: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for 'alg: none' JWT, got {response.status_code}"

def test_alg_none_upper_jwt_rejected(none_upper_jwt):
    headers = {"Authorization": f"Bearer {none_upper_jwt}"}
    try:
        response = requests.get("http://127.0.0.1:8080/data", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the proxy: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for 'alg: NONE' JWT, got {response.status_code}"

def test_blocked_requests_log():
    log_path = "/app/blocked_reqs.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist"

    # Check permissions (0600)
    st = os.stat(log_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Expected permissions 0o600 for {log_path}, got {oct(perms)}"

    # Check content
    with open(log_path, "r") as f:
        content = f.read()
    assert "Blocked JWT attempt" in content, f"Log file {log_path} does not contain 'Blocked JWT attempt'"