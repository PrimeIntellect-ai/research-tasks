# test_final_state.py
import requests
import hashlib
import json
import os
import pytest

def test_server_valid_request():
    url = "http://127.0.0.1:8080/report"
    headers = {
        "Authorization": "Bearer SUPER_SECRET_PENTEST_TOKEN_99",
        "Content-Type": "application/json"
    }
    payload = {
        "xss_payload": "<script>alert(1)</script>",
        "victim_email": "ceo@company.local"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert data.get("status") == "analyzed", f"Expected status 'analyzed', got {data.get('status')}"
    assert data.get("redacted_email") == "[REDACTED]", f"Expected redacted_email '[REDACTED]', got {data.get('redacted_email')}"

    expected_hash = hashlib.sha256(payload["xss_payload"].encode('utf-8')).hexdigest()
    assert data.get("payload_hash") == expected_hash, f"Expected payload_hash {expected_hash}, got {data.get('payload_hash')}"

def test_server_invalid_auth():
    url = "http://127.0.0.1:8080/report"
    headers = {
        "Authorization": "Bearer WRONG_TOKEN",
        "Content-Type": "application/json"
    }
    payload = {
        "xss_payload": "test",
        "victim_email": "test@test.com"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for invalid auth, got {response.status_code}. Response: {response.text}"

def test_server_missing_auth():
    url = "http://127.0.0.1:8080/report"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "xss_payload": "test",
        "victim_email": "test@test.com"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for missing auth, got {response.status_code}. Response: {response.text}"

def test_server_log_exists():
    log_path = "/home/user/server.log"
    assert os.path.isfile(log_path), f"Expected server log file not found at {log_path}. Ensure logs are written to this exact path."