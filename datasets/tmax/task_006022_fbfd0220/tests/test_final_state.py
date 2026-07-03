# test_final_state.py

import os
import json
import subprocess
import pytest

def test_supervisord_running():
    """Verify that supervisord is running."""
    try:
        result = subprocess.run(['pgrep', 'supervisord'], capture_output=True, text=True)
        assert result.returncode == 0, "supervisord process is not running."
        assert result.stdout.strip(), "No PID found for supervisord."
    except FileNotFoundError:
        pytest.fail("pgrep command not found.")

def test_haproxy_running():
    """Verify that haproxy is running."""
    try:
        result = subprocess.run(['pgrep', 'haproxy'], capture_output=True, text=True)
        assert result.returncode == 0, "haproxy process is not running."
        assert result.stdout.strip(), "No PID found for haproxy."
    except FileNotFoundError:
        pytest.fail("pgrep command not found.")

def test_haproxy_cfg_permissions():
    """Verify that /home/user/haproxy/haproxy.cfg has exactly 400 permissions."""
    cfg_path = "/home/user/haproxy/haproxy.cfg"
    assert os.path.isfile(cfg_path), f"HAProxy configuration file not found at {cfg_path}."

    stat_info = os.stat(cfg_path)
    permissions = stat_info.st_mode & 0o777
    assert permissions == 0o400, f"Expected permissions 400, but got {oct(permissions)} for {cfg_path}."

def test_health_log_contents():
    """Verify that /home/user/health_log.txt exists and contains the correct JSON."""
    log_path = "/home/user/health_log.txt"
    assert os.path.isfile(log_path), f"Health log file not found at {log_path}."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content, f"File {log_path} is empty."

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Content of {log_path} is not valid JSON. Content: {content}")

    assert data.get("status") == "UP", f"Expected status 'UP', got {data.get('status')}."
    assert data.get("uptime") == 9999, f"Expected uptime 9999, got {data.get('uptime')}."