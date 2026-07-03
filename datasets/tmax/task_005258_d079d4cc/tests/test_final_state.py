# test_final_state.py

import os
import re
import subprocess
import time
import urllib.request
import pytest

def test_directories_exist():
    dirs = [
        "/home/user/run",
        "/home/user/logs",
        "/home/user/alerts"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} does not exist."

def test_deploy_script_and_forwarder():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"Deploy script {deploy_script} not found."
    assert os.access(deploy_script, os.X_OK), f"{deploy_script} is not executable."

    pid_file = "/home/user/run/forwarder.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} not found. Did deploy.sh run?"

    with open(pid_file, "r") as f:
        pid = f.read().strip()

    assert pid.isdigit(), f"PID file {pid_file} does not contain a valid PID."

    # Check if process is running
    assert os.path.exists(f"/proc/{pid}"), f"Process with PID {pid} is not running."

    with open(f"/proc/{pid}/comm", "r") as f:
        comm = f.read().strip()
    assert "socat" in comm, f"Process {pid} is not socat, it is {comm}."

    # Start a dummy python server on 9090 to test forwarding
    server_proc = subprocess.Popen(["python3", "-m", "http.server", "9090", "--bind", "127.0.0.1"])
    time.sleep(1) # wait for server to bind

    try:
        req = urllib.request.Request("http://127.0.0.1:8080/")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, "Forwarder did not return 200 OK."
    finally:
        server_proc.terminate()
        server_proc.wait()

def test_health_check_script():
    script = "/home/user/health_check.sh"
    log_file = "/home/user/logs/health.log"

    assert os.path.isfile(script), f"Health check script {script} not found."
    assert os.access(script, os.X_OK), f"{script} is not executable."

    # Start python server
    server_proc = subprocess.Popen(["python3", "-m", "http.server", "9090", "--bind", "127.0.0.1"])
    time.sleep(1)

    try:
        subprocess.run([script], check=True)
        assert os.path.isfile(log_file), f"Log file {log_file} not created."
        with open(log_file, "r") as f:
            content = f.read()
        assert re.search(r"\[\d+\] STATUS: OK", content), "Log file does not contain STATUS: OK when server is up."
    finally:
        server_proc.terminate()
        server_proc.wait()

    # Now test with server down
    subprocess.run([script], check=True)
    with open(log_file, "r") as f:
        content = f.read()
    assert re.search(r"\[\d+\] STATUS: FAIL", content), "Log file does not contain STATUS: FAIL when server is down."

def test_logrotate_config():
    conf = "/home/user/logrotate.conf"
    assert os.path.isfile(conf), f"Logrotate config {conf} not found."

    with open(conf, "r") as f:
        content = f.read()

    assert re.search(r"size\s+10k", content, re.IGNORECASE), "logrotate.conf does not contain 'size 10k'."
    assert re.search(r"rotate\s+3", content, re.IGNORECASE), "logrotate.conf does not contain 'rotate 3'."
    assert "/home/user/logs/health.log" in content, "logrotate.conf does not target /home/user/logs/health.log."

def test_storage_monitor_script():
    script = "/home/user/storage_monitor.sh"
    alert_file = "/home/user/alerts/quota.txt"
    log_dir = "/home/user/logs"

    assert os.path.isfile(script), f"Storage monitor script {script} not found."
    assert os.access(script, os.X_OK), f"{script} is not executable."

    # Ensure size is small initially
    subprocess.run([script], check=True)
    assert os.path.isfile(alert_file), f"Alert file {alert_file} not created."
    with open(alert_file, "r") as f:
        assert f.read().strip() == "QUOTA_OK", "Alert file does not say QUOTA_OK when size is small."

    # Create a large dummy file
    dummy_file = os.path.join(log_dir, "dummy.log")
    try:
        with open(dummy_file, "wb") as f:
            f.write(b"0" * 60000) # > 51200 bytes

        subprocess.run([script], check=True)
        with open(alert_file, "r") as f:
            assert f.read().strip() == "QUOTA_EXCEEDED", "Alert file does not say QUOTA_EXCEEDED when size is large."
    finally:
        if os.path.exists(dummy_file):
            os.remove(dummy_file)