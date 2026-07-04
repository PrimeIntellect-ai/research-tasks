# test_final_state.py

import os
import json
import hashlib
import requests
import pytest

def test_decrypted_evidence_exists_and_correct():
    evidence_path = "/home/user/decrypted_evidence.json"
    assert os.path.exists(evidence_path), f"Decrypted evidence file is missing at {evidence_path}"
    assert os.path.isfile(evidence_path), f"Path {evidence_path} is not a file"

    with open(evidence_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {evidence_path} does not contain valid JSON")

    assert "auth_token" in data, "Decrypted JSON missing 'auth_token'"
    assert "listen_port" in data, "Decrypted JSON missing 'listen_port'"

    assert data["auth_token"] == "whiskey_tango_foxtrot_99", "Incorrect auth_token in decrypted JSON"
    assert data["listen_port"] == 8080, "Incorrect listen_port in decrypted JSON"

def test_callback_server_no_auth():
    url = "http://127.0.0.1:8080/callback"
    try:
        response = requests.post(url, data=b"test", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 without Authorization header, got {response.status_code}"

def test_callback_server_wrong_auth():
    url = "http://127.0.0.1:8080/callback"
    headers = {"Authorization": "Bearer wrong_token"}
    try:
        response = requests.post(url, data=b"test", headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 with wrong Authorization header, got {response.status_code}"

def test_callback_server_correct_auth_and_hashing():
    url = "http://127.0.0.1:8080/callback"
    headers = {"Authorization": "Bearer whiskey_tango_foxtrot_99"}
    payload = b"test_payload_123"
    expected_hash = hashlib.sha256(payload).hexdigest()

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 with correct Authorization header, got {response.status_code}. Response: {response.text}"

    try:
        resp_json = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert resp_json.get("status") == "received", f"Expected status 'received', got {resp_json.get('status')}"
    assert resp_json.get("sha256") == expected_hash, f"Expected sha256 '{expected_hash}', got {resp_json.get('sha256')}"