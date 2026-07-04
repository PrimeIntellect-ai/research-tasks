# test_final_state.py

import os
import time
import urllib.request
import urllib.error
import re
import subprocess
import signal
import socket
import pytest

def test_nginx_running():
    """Ensure Nginx is running and pid file exists."""
    pid_file = '/home/user/nginx/nginx.pid'
    assert os.path.exists(pid_file), f"Nginx PID file missing at {pid_file}"

    # Check if port 8080 is listening
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', 8080))
        assert result == 0, "Nginx is not listening on port 8080."

def test_nginx_proxy():
    """Ensure Nginx reverse proxy is working and loading the upstream conf."""
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/health")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8').strip()
            assert body == "OK", f"Expected response body 'OK', got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx proxy on 8080: {e}")

def test_uptime_log_format():
    """Check that uptime.log exists and contains the correct format."""
    log_file = '/home/user/uptime.log'
    assert os.path.exists(log_file), f"Log file missing at {log_file}"

    with open(log_file, 'r') as f:
        lines = f.read().strip().split('\n')
        assert len(lines) > 0, "uptime.log is empty"
        last_line = lines[-1]
        # Format: <EPOCH_TIMESTAMP> | 9001:<UP|DOWN> | 9002:<UP|DOWN> | 9003:<UP|DOWN>
        assert re.match(r'^\d+\s*\|\s*9001:(UP|DOWN)\s*\|\s*9002:(UP|DOWN)\s*\|\s*9003:(UP|DOWN)$', last_line), \
            f"Log format is incorrect. Got: '{last_line}'"

def test_dynamic_update():
    """Kill backend 9002, wait, and verify the monitor updates state properly."""
    # Find and kill the python process listening on 9002
    try:
        ps_output = subprocess.check_output(['ps', 'aux']).decode()
        killed = False
        for line in ps_output.splitlines():
            if 'server.py 9002' in line and 'grep' not in line:
                pid = int(line.split()[1])
                os.kill(pid, signal.SIGKILL)
                killed = True
        assert killed, "Could not find backend process for port 9002 to kill."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run ps command.")

    # Wait for the monitor to detect the failure (checks every 2s)
    time.sleep(3.5)

    # 1. Verify uptime.log registers 9002:DOWN
    log_file = '/home/user/uptime.log'
    assert os.path.exists(log_file), f"Log file missing at {log_file}"
    with open(log_file, 'r') as f:
        lines = f.read().strip().split('\n')
        last_line = lines[-1]
        assert "9002:DOWN" in last_line, f"Expected 9002:DOWN in log after killing it. Got: '{last_line}'"

    # 2. Verify upstream.conf no longer contains 9002
    upstream_file = '/home/user/nginx/upstream.conf'
    assert os.path.exists(upstream_file), f"Upstream conf missing at {upstream_file}"
    with open(upstream_file, 'r') as f:
        content = f.read()
        assert '9002' not in content, f"Port 9002 should have been removed from {upstream_file}"

    # 3. Verify curl to 8080/health still succeeds (served by 9001 or 9003)
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/health")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8').strip()
            assert body == "OK", f"Expected response body 'OK', got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx proxy on 8080 after backend failure: {e}")