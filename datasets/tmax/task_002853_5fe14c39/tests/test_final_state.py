# test_final_state.py

import os
import time
import json
import socket
import subprocess
import requests
import pytest

PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{PORT}/process"
TOKEN = "K83-F9A-X7M"

@pytest.fixture(scope="session", autouse=True)
def ensure_server_running():
    # Check if port is open
    def is_port_open():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((HOST, PORT)) == 0

    if not is_port_open():
        server_path = "/home/user/server.py"
        assert os.path.isfile(server_path), f"Server script not found at {server_path} and port {PORT} is not open."

        proc = subprocess.Popen(["python3", server_path])

        # Wait for port to open
        for _ in range(20):
            if is_port_open():
                break
            time.sleep(0.5)
        else:
            proc.kill()
            pytest.fail(f"Server at {server_path} failed to start or bind to {HOST}:{PORT}")

        yield
        proc.terminate()
    else:
        yield

def test_shared_library_compiled():
    so_path = "/app/legacy_calc/libmatrix_ops.so"
    assert os.path.isfile(so_path), f"Shared library not found at {so_path}. Did you compile the C code?"

def test_process_authenticated_success():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"value": 10.0}

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"

    result = data.get("result")
    assert result is not None, "Response JSON missing 'result' field."

    expected_result = 131.4159
    assert abs(result - expected_result) < 0.0001, f"Expected result {expected_result}, got {result}"

def test_process_missing_auth():
    headers = {
        "Content-Type": "application/json"
    }
    payload = {"value": 10.0}

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert response.status_code == 401, f"Expected status 401 for missing auth, got {response.status_code}. Response: {response.text}"

def test_process_invalid_auth():
    headers = {
        "Authorization": "Bearer INVALID-TOKEN",
        "Content-Type": "application/json"
    }
    payload = {"value": 10.0}

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert response.status_code == 401, f"Expected status 401 for invalid auth, got {response.status_code}. Response: {response.text}"