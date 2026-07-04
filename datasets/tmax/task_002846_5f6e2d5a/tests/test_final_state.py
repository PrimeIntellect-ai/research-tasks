# test_final_state.py

import os
import stat
import subprocess
import requests
import pytest
import json

APP_DIR = "/home/user/app"
DATA_DIR = os.path.join(APP_DIR, "data")
DEPLOY_SCRIPT = os.path.join(APP_DIR, "deploy.sh")
SOCKET_FILE = os.path.join(APP_DIR, "backend.sock")
SERVER_BIN = os.path.join(APP_DIR, "server")

def get_total_data_bytes(directory):
    total_size = 0
    for root, _, files in os.walk(directory):
        for f in files:
            file_path = os.path.join(root, f)
            if os.path.isfile(file_path) and not os.path.islink(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

def test_deploy_script_exists_and_executable():
    assert os.path.isfile(DEPLOY_SCRIPT), f"Deployment script {DEPLOY_SCRIPT} does not exist."
    st = os.stat(DEPLOY_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deployment script {DEPLOY_SCRIPT} is not executable."

def test_go_server_running():
    try:
        output = subprocess.check_output(["ps", "aux"]).decode()
        assert "server" in output or SERVER_BIN in output, f"The Go backend daemon ({SERVER_BIN}) is not running."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps command to check running processes.")

def test_unix_socket_exists():
    # The prompt says: "Verifier will check that /home/user/app/backend.sock exists and is a valid Unix socket."
    assert os.path.exists(SOCKET_FILE), f"Unix socket {SOCKET_FILE} does not exist."
    mode = os.stat(SOCKET_FILE).st_mode
    assert stat.S_ISSOCK(mode), f"File {SOCKET_FILE} is not a valid Unix socket."

def test_status_endpoint():
    expected_bytes = get_total_data_bytes(DATA_DIR)

    url = "http://127.0.0.1:8080/status"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    assert "data_bytes" in data, f"Key 'data_bytes' missing from JSON response. Response: {data}"
    assert data["data_bytes"] == expected_bytes, f"Expected 'data_bytes' to be {expected_bytes}, got {data['data_bytes']}."