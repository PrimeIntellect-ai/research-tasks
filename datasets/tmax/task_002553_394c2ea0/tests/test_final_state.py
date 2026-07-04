# test_final_state.py

import os
import json
import socket
import subprocess
import requests

def test_directory_structure_and_symlink():
    """Verify that the required directories and symlink are created correctly."""
    v1_dir = "/home/user/telemetry_app/releases/v1"
    logs_dir = "/home/user/telemetry_app/logs"
    current_symlink = "/home/user/telemetry_app/current"

    assert os.path.isdir(v1_dir), f"Directory {v1_dir} is missing or not a directory."
    assert os.path.isdir(logs_dir), f"Directory {logs_dir} is missing or not a directory."

    assert os.path.islink(current_symlink), f"{current_symlink} is not a symlink."
    target = os.readlink(current_symlink)
    # The target might be absolute or relative, but it must resolve to v1_dir
    assert os.path.abspath(os.path.join("/home/user/telemetry_app", target)) == os.path.abspath(v1_dir), \
        f"Symlink {current_symlink} does not point to {v1_dir}."

def test_status_json():
    """Verify the content of status.json."""
    status_file = "/home/user/telemetry_app/releases/v1/status.json"
    assert os.path.isfile(status_file), f"File {status_file} is missing."

    with open(status_file, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
        assert data == {"status": "provisioned"}, f"status.json content is incorrect: {data}"
    except json.JSONDecodeError:
        assert False, f"status.json does not contain valid JSON: {content}"

def test_http_service():
    """Verify the HTTP service is serving status.json correctly."""
    url = "http://127.0.0.1:9080/status.json"
    try:
        response = requests.get(url, timeout=2)
        assert response.status_code == 200, f"HTTP GET {url} returned status {response.status_code}."
        data = response.json()
        assert data == {"status": "provisioned"}, f"HTTP response JSON is incorrect: {data}"
    except requests.RequestException as e:
        assert False, f"HTTP service check failed: {e}"

def test_tcp_auth_service():
    """Verify the TCP auth service responds correctly to valid and invalid PINs."""
    host = "127.0.0.1"
    port = 9081

    # Test valid PIN
    try:
        with socket.create_connection((host, port), timeout=2) as s:
            s.sendall(b"4092\n")
            response = s.recv(1024).decode("utf-8")
            assert response == "AUTH_OK\n", f"Expected 'AUTH_OK\\n' for valid PIN, got {repr(response)}"
    except Exception as e:
        assert False, f"TCP valid PIN test failed: {e}"

    # Test invalid PIN
    try:
        with socket.create_connection((host, port), timeout=2) as s:
            s.sendall(b"9999\n")
            response = s.recv(1024).decode("utf-8")
            assert response == "AUTH_FAIL\n", f"Expected 'AUTH_FAIL\\n' for invalid PIN, got {repr(response)}"
    except Exception as e:
        assert False, f"TCP invalid PIN test failed: {e}"

def test_expect_script():
    """Verify the expect script exists and contains the correct PIN."""
    script_path = "/home/user/telemetry_app/health_check.exp"
    assert os.path.isfile(script_path), f"Expect script missing at {script_path}."

    with open(script_path, "r") as f:
        content = f.read()

    assert "4092" in content, f"Expect script does not contain the extracted PIN '4092'."
    assert "AUTH_OK" in content, f"Expect script does not contain the expected 'AUTH_OK' string."

def test_cron_job():
    """Verify the crontab contains the correct scheduled task."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        assert False, "Failed to read crontab. No crontab for user?"

    # Check for 5-minute interval and correct command/redirect
    assert "*/5" in crontab_output or "0,5,10" in crontab_output or "5 * * * *" in crontab_output, \
        "Crontab does not seem to run every 5 minutes."
    assert "/home/user/telemetry_app/health_check.exp" in crontab_output, \
        "Crontab does not execute health_check.exp."
    assert "/home/user/telemetry_app/logs/health.log" in crontab_output, \
        "Crontab does not redirect to health.log."