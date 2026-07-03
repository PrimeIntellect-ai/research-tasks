# test_final_state.py

import os
import urllib.request
import subprocess
import pytest

def test_nginx_config():
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "proxy_pass http://127.0.0.1:8081" in content or "proxy_pass http://localhost:8081" in content, \
        "nginx.conf does not proxy to port 8081"

def test_nginx_running():
    pid_path = "/home/user/nginx.pid"
    assert os.path.isfile(pid_path), f"Nginx pid file {pid_path} is missing, Nginx might not be running"

    with open(pid_path, "r") as f:
        pid = f.read().strip()

    assert pid.isdigit(), f"Invalid PID in {pid_path}"

    # Check if process is running
    try:
        os.kill(int(pid), 0)
    except OSError:
        pytest.fail(f"Nginx process with PID {pid} is not running")

def test_monitor_script():
    script_path = "/home/user/app/monitor.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

    with open(script_path, "r") as f:
        content = f.read()

    assert "server.py" in content, "monitor.sh does not reference server.py"
    assert "server.log" in content, "monitor.sh does not redirect to server.log"

def test_success_txt():
    success_path = "/home/user/success.txt"
    assert os.path.isfile(success_path), f"File {success_path} is missing"

    with open(success_path, "r") as f:
        content = f.read()

    assert content == "Backend Service Operational\n", "success.txt does not contain the exact expected output"

def test_services_reachable():
    # Test Nginx proxy
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8080/", timeout=2)
        response = req.read().decode("utf-8")
        assert response == "Backend Service Operational\n", "Nginx did not return the expected backend response"
    except Exception as e:
        pytest.fail(f"Failed to reach backend via Nginx on port 8080: {e}")