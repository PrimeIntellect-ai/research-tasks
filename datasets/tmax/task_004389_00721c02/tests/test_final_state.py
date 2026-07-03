# test_final_state.py

import os
import tarfile
import subprocess
import socket
import json
import pytest
import requests
import tempfile
import glob

def test_downtime_backup():
    """Verify the downtime backup archive exists and contains exactly 45 PNG files."""
    archive_path = "/home/user/downtime_backup.tar.gz"
    assert os.path.exists(archive_path), f"Archive not found: {archive_path}"
    assert tarfile.is_tarfile(archive_path), f"Not a valid tar archive: {archive_path}"

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        # Find all png files recursively
        png_files = []
        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                if file.lower().endswith(".png"):
                    png_files.append(os.path.join(root, file))

        assert len(png_files) == 45, f"Expected exactly 45 PNG files in archive, found {len(png_files)}"

def test_expect_script():
    """Verify the expect script runs successfully and dispatches the alert."""
    script_path = "/home/user/alert.exp"
    assert os.path.exists(script_path), f"Expect script not found: {script_path}"

    try:
        result = subprocess.run(["expect", script_path], capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        pytest.fail("Expect script timed out.")

    assert result.returncode == 0, f"Expect script failed with exit code {result.returncode}. Output: {result.stdout}"
    assert "Alert dispatched successfully." in result.stdout, f"Alert was not dispatched successfully. Output: {result.stdout}"

def test_http_service():
    """Verify the HTTP service on port 8080 returns the correct JSON payload."""
    url = "http://127.0.0.1:8080/api/status"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "uptime_percent" in data, f"Key 'uptime_percent' not found in JSON: {data}"

    uptime = float(data["uptime_percent"])
    assert uptime == 85.0, f"Expected uptime_percent to be 85.0, got {uptime}"

def test_tcp_service():
    """Verify the TCP service on port 8081 returns the correct string."""
    host = "127.0.0.1"
    port = 8081

    try:
        with socket.create_connection((host, port), timeout=2) as sock:
            data = sock.recv(1024).decode('utf-8')
    except (socket.timeout, ConnectionRefusedError) as e:
        pytest.fail(f"TCP connection failed: {e}")

    expected_response = "UPTIME:85.00\n"
    assert data == expected_response, f"Expected TCP response '{expected_response}', got '{data}'"