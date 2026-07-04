# test_final_state.py

import os
import stat
import json
import base64
import hmac
import hashlib
import requests
import pytest

def test_secret_key_permissions():
    path = "/home/user/keys/secret.key"
    assert os.path.isfile(path), f"Secret key file missing: {path}"
    st = os.stat(path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Secret key permissions are {oct(perms)}, expected 0o400. File permissions policy not enforced."

def test_server_no_auth():
    try:
        resp = requests.get("http://127.0.0.1:8000/data", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")
    assert resp.status_code == 401, f"Expected HTTP 401 for request without Authorization header, got {resp.status_code}"

def test_server_alg_none():
    header = {"alg": "none", "typ": "JWT"}
    payload = {"user": "test"}

    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')

    token = f"{header_b64}.{payload_b64}."

    try:
        resp = requests.get("http://127.0.0.1:8000/data", headers={"Authorization": f"Bearer {token}"}, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp.status_code == 401, f"Expected HTTP 401 for token with alg='none', got {resp.status_code}. The vulnerability bypass is likely still active."

def test_server_valid_token():
    path = "/home/user/keys/secret.key"
    assert os.path.isfile(path), f"Secret key file missing: {path}"

    with open(path, "r") as f:
        secret = f.read().strip()

    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"user": "test"}

    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')

    msg = f"{header_b64}.{payload_b64}"
    sig = hmac.new(secret.encode(), msg.encode(), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode().rstrip('=')

    token = f"{msg}.{sig_b64}"

    try:
        resp = requests.get("http://127.0.0.1:8000/data", headers={"Authorization": f"Bearer {token}"}, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200 for valid signed token, got {resp.status_code}"