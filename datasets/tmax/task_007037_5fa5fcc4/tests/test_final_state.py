# test_final_state.py
import os
import urllib.request
import subprocess
import re
import pytest

def test_start_backends_script_fixed():
    """Test that start_backends.sh is fixed to use the correct ports and bind addresses."""
    script_path = "/home/user/capacity_planner/start_backends.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert re.search(r'8081\s+--bind\s+127\.0\.0\.1', content), "Port 8081 not bound to 127.0.0.1 in start_backends.sh"
    assert re.search(r'8082\s+--bind\s+127\.0\.0\.1', content), "Port 8082 not bound to 127.0.0.1 in start_backends.sh"
    assert re.search(r'8083\s+--bind\s+127\.0\.0\.1', content), "Port 8083 not bound to 127.0.0.1 in start_backends.sh"

def test_python_servers_running():
    """Test that python HTTP servers are listening on 8081, 8082, 8083."""
    for port in [8081, 8082, 8083]:
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{port}/")
            with urllib.request.urlopen(req, timeout=2) as response:
                assert response.status == 200, f"Server on port {port} returned status {response.status}"
                body = response.read().decode('utf-8')
                assert "Directory listing" in body or "Directory" in body, f"Server on port {port} not serving directory listing"
        except Exception as e:
            pytest.fail(f"Could not connect to python server on 127.0.0.1:{port}: {e}")

def test_haproxy_cfg_fixed():
    """Test that haproxy.cfg is fixed to listen on 8080 and point to correct backends."""
    cfg_path = "/home/user/capacity_planner/haproxy.cfg"
    assert os.path.isfile(cfg_path), f"Config file {cfg_path} does not exist."

    with open(cfg_path, "r") as f:
        content = f.read()

    assert re.search(r'bind\s+127\.0\.0\.1:8080', content), "HAProxy frontend not bound to 127.0.0.1:8080"
    assert re.search(r'127\.0\.0\.1:8081', content), "HAProxy backend missing 127.0.0.1:8081"
    assert re.search(r'127\.0\.0\.1:8082', content), "HAProxy backend missing 127.0.0.1:8082"
    assert re.search(r'127\.0\.0\.1:8083', content), "HAProxy backend missing 127.0.0.1:8083"

def test_haproxy_running():
    """Test that HAProxy is running and listening on 127.0.0.1:8080."""
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"HAProxy on port 8080 returned status {response.status}"
            body = response.read().decode('utf-8')
            assert "Directory" in body, "HAProxy did not return the backend directory listing"
    except Exception as e:
        pytest.fail(f"Could not connect to HAProxy on 127.0.0.1:8080: {e}")

def test_check_capacity_script():
    """Test that check_capacity.sh exists, is executable, and contains the correct commands."""
    script_path = "/home/user/capacity_planner/check_capacity.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "curl" in content and "-s" in content, "check_capacity.sh must use curl in silent mode"
    assert "127.0.0.1:8080" in content, "check_capacity.sh must curl 127.0.0.1:8080"
    assert "capacity_log.txt" in content, "check_capacity.sh must append to capacity_log.txt"

def test_capacity_log():
    """Test that capacity_log.txt exists and contains the HTML response."""
    log_path = "/home/user/capacity_planner/capacity_log.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run the script?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "<html" in content.lower() or "directory" in content.lower(), f"Log file {log_path} does not contain the expected HTML response."

def test_crontab_txt():
    """Test that crontab.txt contains the correct cron schedule."""
    crontab_path = "/home/user/capacity_planner/crontab.txt"
    assert os.path.isfile(crontab_path), f"File {crontab_path} does not exist."

    with open(crontab_path, "r") as f:
        content = f.read().strip()

    assert re.search(r'\*/5\s+\*\s+\*\s+\*\s+\*\s+/home/user/capacity_planner/check_capacity\.sh', content), \
        f"crontab.txt does not contain the correct schedule. Found: {content}"