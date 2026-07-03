# test_final_state.py

import os
import json
import base64
import requests
import pytest

def test_recovered_key_file():
    """Verify that the recovered key is written correctly."""
    path = "/app/recovered_key.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "WntrBse_xk", f"Recovered key is incorrect. Got: {content}"

def test_audit_file():
    """Verify that the audit file contains the correct CWE identifier."""
    path = "/app/audit.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert "CWE-214" in content.upper(), f"Audit file does not contain CWE-214. Got: {content}"

def test_service_unauthorized():
    """Verify that the service returns 401 for missing or invalid tokens."""
    url = "http://127.0.0.1:8080/rotate"
    payload = {"new_key": "test_key"}

    # Missing token
    try:
        resp = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert resp.status_code == 401, f"Expected 401 for missing token, got {resp.status_code}"

    # Invalid token
    headers = {"Authorization": "Bearer WntrBse_xx"}
    resp = requests.post(url, json=payload, headers=headers, timeout=2)
    assert resp.status_code == 401, f"Expected 401 for invalid token, got {resp.status_code}"

def test_service_rotate_success():
    """Verify that the service successfully rotates credentials and returns the expected structure."""
    url = "http://127.0.0.1:8080/rotate"
    payload = {"new_key": "SecureN3wK3y!"}
    headers = {"Authorization": "Bearer WntrBse_xk"}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "encrypted_credentials" in data, "Response JSON missing 'encrypted_credentials' key."

    b64_ct = data["encrypted_credentials"]
    try:
        ct_bytes = base64.b64decode(b64_ct)
    except Exception:
        pytest.fail(f"encrypted_credentials is not valid base64: {b64_ct}")

    # Original JSON: {"db_user":"admin","db_pass":"sUp3rS3cr3tDBP@ss"} -> 53 bytes
    # AES-GCM tag -> 16 bytes
    # Total expected length -> 69 bytes
    expected_length = 53 + 16
    assert len(ct_bytes) == expected_length, f"Expected ciphertext length {expected_length}, got {len(ct_bytes)}"