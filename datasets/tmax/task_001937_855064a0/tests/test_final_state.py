# test_final_state.py

import os
import socket
import requests
import json
import math
import subprocess

def test_watchdog_script_exists_and_executable():
    """Test that the watchdog script exists and is executable."""
    script_path = "/home/user/watchdog.sh"
    assert os.path.exists(script_path), f"Watchdog script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Watchdog script {script_path} is not executable."

def test_log_file_exists():
    """Test that the restore service log file exists."""
    log_path = "/home/user/restore_service.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. The service might not be running or logging correctly."

def test_http_api_unauthorized():
    """Test that the HTTP API returns 401 when unauthorized."""
    url = "http://127.0.0.1:8080/api/v1/audio-meta"
    try:
        response = requests.get(url, timeout=2)
        assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    except requests.RequestException as e:
        assert False, f"HTTP request failed: {e}"

def test_http_api_authorized():
    """Test that the HTTP API returns the correct JSON when authorized."""
    url = "http://127.0.0.1:8080/api/v1/audio-meta"
    headers = {"Authorization": "Bearer operator-token-8831"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

        data = response.json()
        assert "filepath" in data, "Response JSON missing 'filepath'"
        assert data["filepath"] == "/app/voicemail_backup.wav", f"Expected filepath '/app/voicemail_backup.wav', got {data['filepath']}"

        assert "size_bytes" in data, "Response JSON missing 'size_bytes'"

        # Verify size matches actual file size
        actual_size = os.path.getsize("/app/voicemail_backup.wav")
        assert data["size_bytes"] == actual_size, f"Expected size_bytes {actual_size}, got {data['size_bytes']}"

        assert "duration_seconds" in data, "Response JSON missing 'duration_seconds'"
        # Expected duration is ~12.45
        assert math.isclose(data["duration_seconds"], 12.45, abs_tol=0.15), f"Expected duration_seconds ~12.45, got {data['duration_seconds']}"

    except requests.RequestException as e:
        assert False, f"HTTP request failed: {e}"
    except ValueError:
        assert False, f"Failed to parse JSON response: {response.text}"

def test_tcp_health_check():
    """Test the TCP health check endpoint."""
    host = "127.0.0.1"
    port = 8081

    try:
        with socket.create_connection((host, port), timeout=2) as s:
            s.sendall(b"STATUS\n")
            data = s.recv(1024)
            assert data == b"OK\n", f"Expected 'OK\\n', got {data!r}"

            # Check if connection is closed by server
            # If closed, recv should return empty bytes
            extra_data = s.recv(1024)
            assert extra_data == b"", "Expected connection to be closed by server, but it remained open."

    except (socket.timeout, ConnectionRefusedError) as e:
        assert False, f"TCP connection failed: {e}"

def test_watchdog_running():
    """Test that watchdog.sh is currently running."""
    try:
        output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
        assert "watchdog.sh" in output, "watchdog.sh does not appear to be running in the background."
    except subprocess.CalledProcessError:
        pass # Ignore if ps aux fails for some reason