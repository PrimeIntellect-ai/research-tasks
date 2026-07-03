# test_final_state.py

import os
import socket
import pytest
import requests

def test_run_all_script_exists_and_executable():
    script_path = "/home/user/run_all.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_http_api_status():
    url = "http://127.0.0.1:8080/api/status"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP API at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, but got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response from {url}, but got: {response.text}")

    assert data.get("status") == "ok", f"Expected 'status' to be 'ok', got: {data.get('status')}"
    assert data.get("db_connected") is True, f"Expected 'db_connected' to be True, got: {data.get('db_connected')}"

def test_tcp_data_service():
    host = "127.0.0.1"
    port = 8081
    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(b"PING\n")
            data = s.recv(1024)
    except Exception as e:
        pytest.fail(f"Failed to connect and communicate with the TCP data service at {host}:{port}. Error: {e}")

    response_text = data.decode('utf-8', errors='replace')
    expected_response = "PONG: DATA_READY"
    assert expected_response in response_text, f"Expected TCP response to contain '{expected_response}', but got: {response_text.strip()}"

def test_extracted_files_exist():
    config_path = "/home/user/app/config.json"
    db_path = "/home/user/app/data.db"

    assert os.path.exists(config_path), f"Configuration file missing at {config_path}. Was the backup extracted?"
    assert os.path.exists(db_path), f"Database file missing at {db_path}. Was the backup extracted?"