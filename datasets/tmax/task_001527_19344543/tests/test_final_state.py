# test_final_state.py
import os
import socket
import requests
import pytest

def test_supervisor_script():
    script_path = "/home/user/supervisor.sh"
    assert os.path.exists(script_path), f"Supervisor script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Supervisor script at {script_path} is not executable"

def test_raw_tcp_status():
    host = "127.0.0.1"
    port = 9001
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            sock.sendall(b"STATUS\n")
            response = sock.recv(1024)
            assert response == b"OK\n", f"Expected 'OK\\n' from raw TCP status, got {response!r}"
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused to {host}:{port}. Is the raw TCP server running?")
    except socket.timeout:
        pytest.fail(f"Connection to {host}:{port} timed out.")

def test_http_process_and_backup():
    url = "http://127.0.0.1:8080/process"
    try:
        response = requests.get(url, timeout=30)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Failed to connect to Nginx at {url}. Is Nginx running and configured correctly?")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {url} timed out.")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "red_frames" in data, "Response JSON missing 'red_frames' key"
    assert data["red_frames"] == 3, f"Expected 3 red frames, got {data['red_frames']}"

    backup_path = "/home/user/backup/frames.tar.gz"
    assert os.path.exists(backup_path), f"Backup archive not found at {backup_path} after processing"
    assert os.path.isfile(backup_path), f"Backup path {backup_path} is not a file"
    assert os.path.getsize(backup_path) > 0, f"Backup archive at {backup_path} is empty"