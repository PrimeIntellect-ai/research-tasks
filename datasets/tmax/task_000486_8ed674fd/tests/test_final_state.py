# test_final_state.py

import os
import stat
import urllib.request
import ssl
import subprocess
import time
import json
import pytest

def test_permissions():
    """Test that the permissions of the accounts_data directory are exactly 0700."""
    path = "/home/user/accounts_data"
    assert os.path.exists(path), f"Directory {path} does not exist."
    mode = stat.S_IMODE(os.stat(path).st_mode)
    assert mode == 0o700, f"Expected permissions 0700 for {path}, but got {oct(mode)}."

def test_certificates():
    """Test that the TLS certificates exist."""
    cert_path = "/home/user/app/cert.pem"
    key_path = "/home/user/app/key.pem"
    assert os.path.isfile(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Key file {key_path} does not exist."

def test_https_server():
    """Test that the HTTPS server is running and serving the correct data."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request("https://127.0.0.1:8443/users.json")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            assert data == {"users": ["admin", "guest"]}, "Server did not return the expected JSON data."
    except Exception as e:
        pytest.fail(f"HTTPS server check failed: {e}")

def test_supervisor():
    """Test that the supervisor restarts the server and logs the event."""
    # Find server.py pid
    try:
        output = subprocess.check_output(["pgrep", "-f", "server.py"]).decode('utf-8').strip()
        pids = [p for p in output.split('\n') if p]
    except subprocess.CalledProcessError:
        pytest.fail("server.py is not running.")

    assert len(pids) > 0, "No process found for server.py."
    pid = int(pids[0])

    # Kill the server process
    try:
        os.kill(pid, 9)
    except OSError as e:
        pytest.fail(f"Failed to kill server.py (PID {pid}): {e}")

    # Wait for the supervisor to restart it
    time.sleep(3)

    # Check if a new server.py process is running
    try:
        new_output = subprocess.check_output(["pgrep", "-f", "server.py"]).decode('utf-8').strip()
        new_pids = [p for p in new_output.split('\n') if p]
    except subprocess.CalledProcessError:
        pytest.fail("server.py did not restart after being killed.")

    assert str(pid) not in new_pids, "server.py was not actually killed."
    assert len(new_pids) > 0, "server.py did not restart."

    # Check the supervisor log
    log_path = "/home/user/app/supervisor.log"
    assert os.path.isfile(log_path), f"Supervisor log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    assert "[RESTART]" in content, f"Supervisor log {log_path} does not contain the string '[RESTART]'."

    # Check the endpoint again to ensure the restarted server is functional
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request("https://127.0.0.1:8443/users.json")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, "Restarted server did not respond with status 200."
            data = json.loads(response.read().decode('utf-8'))
            assert data == {"users": ["admin", "guest"]}, "Restarted server did not return the expected JSON data."
    except Exception as e:
        pytest.fail(f"HTTPS server not responding correctly after restart: {e}")