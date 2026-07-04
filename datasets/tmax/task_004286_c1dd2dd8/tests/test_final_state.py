# test_final_state.py

import os
import re
import subprocess
import requests
import time
import pytest

def test_acls():
    """Verify ACLs on app_data and logs directories."""
    directories = ["/home/user/app_data", "/home/user/logs"]
    for d in directories:
        assert os.path.isdir(d), f"Directory {d} does not exist"
        result = subprocess.run(["getfacl", d], capture_output=True, text=True)
        assert result.returncode == 0, f"Failed to run getfacl on {d}"
        output = result.stdout
        # Check default group and other
        assert re.search(r"default:group:users:r--", output), f"Default group ACL incorrect on {d}"
        assert re.search(r"default:other::---", output), f"Default other ACL incorrect on {d}"

def test_supervisor_and_process():
    """Verify supervisord and video_server are running."""
    ps_output = subprocess.run(["ps", "aux"], capture_output=True, text=True).stdout
    assert "supervisord" in ps_output, "supervisord is not running"
    assert "video_server" in ps_output, "video_server is not running"

def test_logrotate_config():
    """Verify logrotate configuration."""
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"Logrotate config {conf_path} does not exist"
    with open(conf_path, "r") as f:
        content = f.read()
    assert "/home/user/logs/server.log" in content, "Logrotate config does not target server.log"
    assert "daily" in content, "Logrotate config missing 'daily'"
    assert re.search(r"rotate\s+5", content), "Logrotate config missing 'rotate 5'"
    assert "compress" in content, "Logrotate config missing 'compress'"
    assert "copytruncate" in content, "Logrotate config missing 'copytruncate'"

def test_http_server():
    """Verify the HTTP server behavior."""
    url = "http://127.0.0.1:8080/anomaly"
    headers = {"Authorization": "Bearer factory-edge-token-99"}

    # Test valid request
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    assert response.text.strip() == "142", f"Expected body '142', got '{response.text}'"

    # Test unauthorized request
    response = requests.get(url, timeout=5)
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

    # Test not found
    response = requests.get("http://127.0.0.1:8080/invalid_path", headers=headers, timeout=5)
    assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}"

def test_server_logs():
    """Verify the server log format and timezone."""
    log_path = "/home/user/logs/server.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist"

    with open(log_path, "r") as f:
        logs = f.readlines()

    assert len(logs) > 0, "Log file is empty"

    # Check format: [YYYY-MM-DD HH:MM:SS] <path> <status_code>
    log_pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] /\S+ \d{3}")
    for line in logs:
        assert log_pattern.search(line), f"Log line format incorrect: {line.strip()}"