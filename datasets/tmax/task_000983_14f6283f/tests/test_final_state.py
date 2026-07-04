# test_final_state.py

import os
import time
import socket
import pytest
import requests

def test_start_script_and_log_exist():
    script_path = '/home/user/log-pipeline/start_all.sh'
    log_path = '/home/user/log-pipeline/app.log'

    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"
    assert os.path.isfile(log_path), f"{log_path} does not exist"

def test_rust_service_listening():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('127.0.0.1', 9090))
    sock.close()
    assert result == 0, "Rust TCP service is not listening on 127.0.0.1:9090"

def test_python_gateway_listening():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('127.0.0.1', 8080))
    sock.close()
    assert result == 0, "Python HTTP gateway is not listening on 127.0.0.1:8080"

def test_gateway_missing_auth():
    url = "http://127.0.0.1:8080/ingest"
    response = requests.post(url, data="[INFO] Test message")
    assert response.status_code in [400, 401, 403], f"Expected auth failure status code, got {response.status_code}"

def test_gateway_valid_request():
    url = "http://127.0.0.1:8080/ingest"
    headers = {"Authorization": "Bearer valid-token-1"}
    body = "[ERROR] Connection failed at 10:45"

    response = requests.post(url, headers=headers, data=body)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("severity") == "ERROR", f"Expected severity 'ERROR', got {data.get('severity')}"
    assert data.get("message") == "Connection failed at 10:45", f"Expected message 'Connection failed at 10:45', got {data.get('message')}"

def test_gateway_rate_limiting():
    url = "http://127.0.0.1:8080/ingest"
    headers = {"Authorization": "Bearer rate-limit-token-1"}
    body = "[WARN] Rate limit test"

    # Wait for a fresh second window just in case
    time.sleep(1.1)

    success_count = 0
    too_many_count = 0

    for _ in range(10):
        response = requests.post(url, headers=headers, data=body)
        if response.status_code == 200:
            success_count += 1
        elif response.status_code == 429:
            too_many_count += 1

    assert success_count <= 5, f"Rate limit failed: {success_count} requests succeeded, expected at most 5"
    assert too_many_count >= 5, f"Rate limit failed: {too_many_count} requests returned 429, expected at least 5"

    # Wait for the next second window
    time.sleep(1.1)

    response = requests.post(url, headers=headers, data=body)
    assert response.status_code == 200, f"Expected 200 OK after waiting, got {response.status_code}"