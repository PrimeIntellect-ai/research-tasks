# test_final_state.py

import os
import re
import socket
import subprocess
import requests
import pytest
import time

def test_start_script_fixed():
    start_sh_path = "/app/edge-telemetry/start.sh"
    assert os.path.isfile(start_sh_path), f"{start_sh_path} is missing"

    with open(start_sh_path, "r") as f:
        content = f.read()

    # The typo 'HOSST=' should ideally be fixed, or HOST="0.0.0.0" should be present
    # We check that it doesn't contain the exact buggy line, or that HOST is correctly set.
    # A simple check is that the script no longer contains HOSST= if it was replaced, 
    # but more importantly, the service is running. We can just check that it doesn't have the unmodified bug.
    # Actually, let's just check if HOST="0.0.0.0" or similar is exported, or HOSST is gone.
    assert "HOSST" not in content or "HOST=" in content, "The typo in start.sh does not appear to be fixed."

def test_deploy_script_exists():
    deploy_sh_path = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_sh_path), f"{deploy_sh_path} is missing"
    assert os.access(deploy_sh_path, os.X_OK), f"{deploy_sh_path} is not executable"

def test_logrotate_config():
    logrotate_conf_path = "/home/user/telemetry-logrotate.conf"
    assert os.path.isfile(logrotate_conf_path), f"{logrotate_conf_path} is missing"

    with open(logrotate_conf_path, "r") as f:
        content = f.read()

    assert "/home/user/logs/telemetry.log" in content, "Logrotate config does not target /home/user/logs/telemetry.log"

    # Check for keywords
    keywords = ["daily", "rotate 7", "compress", "missingok", "notifempty"]
    for kw in keywords:
        assert re.search(rf"\b{kw}\b", content), f"Logrotate config missing '{kw}'"

    # Validate with logrotate -d
    result = subprocess.run(["logrotate", "-d", logrotate_conf_path], capture_output=True, text=True)
    assert result.returncode == 0, f"logrotate -d failed: {result.stderr}"

def test_http_health_check():
    url = "http://127.0.0.1:8080/health"
    try:
        response = requests.get(url, timeout=2)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        assert response.json() == {"status": "healthy"}, f"Unexpected response body: {response.text}"
    except requests.RequestException as e:
        pytest.fail(f"HTTP health check failed: {e}")

def test_tcp_ping():
    host = "127.0.0.1"
    port = 8081
    try:
        with socket.create_connection((host, port), timeout=2) as s:
            s.sendall(b"PING\n")
            data = s.recv(1024)
            assert data == b"PONG\n", f"Expected 'PONG\\n', got {data!r}"
    except Exception as e:
        pytest.fail(f"TCP ping failed: {e}")

def test_log_file_exists():
    log_path = "/home/user/logs/telemetry.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist"