# test_final_state.py

import os
import socket
import requests
import pytest
import time

def test_logs_directory_exists():
    assert os.path.isdir("/home/user/logs/"), "The log directory /home/user/logs/ was not created."

def test_scripts_exist_and_executable():
    gateway_path = "/home/user/gateway.py"
    supervise_path = "/home/user/supervise.sh"

    assert os.path.isfile(gateway_path), f"Gateway script missing at {gateway_path}."
    assert os.path.isfile(supervise_path), f"Supervisor script missing at {supervise_path}."

    assert os.access(supervise_path, os.X_OK), f"Supervisor script {supervise_path} is not executable."

def test_http_service_health_authorized():
    url = "http://127.0.0.1:8123/health"
    headers = {"Authorization": "Bearer secure-infra-xyz"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    try:
        data = response.json()
        assert data.get("status") == "ok", f"Expected JSON {{'status': 'ok'}}, got {data}"
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

def test_http_service_health_unauthorized():
    url = "http://127.0.0.1:8123/health"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for missing token, got {response.status_code}"

def test_tcp_echo_service():
    host = "127.0.0.1"
    port = 9321
    message = "test message\n"
    expected_response = "ACK: test message\n"

    try:
        with socket.create_connection((host, port), timeout=2) as s:
            s.sendall(message.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            assert response == expected_response, f"Expected TCP response '{expected_response}', got '{response}'"
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        pytest.fail(f"Failed to connect or communicate with TCP service at {host}:{port}: {e}")