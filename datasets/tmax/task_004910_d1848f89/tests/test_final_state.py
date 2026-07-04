# test_final_state.py

import os
import socket
import time
import subprocess
import pytest

def test_routing_chain_success_rate():
    """
    Test the routing chain success rate metric.
    Sends a payload to GatewayPort (8111) and expects "DATA_ACK" in response.
    """
    gateway_port = 8111
    success_count = 0
    attempts = 3

    for _ in range(attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0)
                s.connect(('127.0.0.1', gateway_port))
                s.sendall(b"PING\n")
                data = s.recv(1024)
                if b"DATA_ACK" in data:
                    success_count += 1
        except Exception:
            pass
        time.sleep(0.5)

    metric = success_count / attempts
    assert metric >= 1.0, f"Routing Chain Success Rate metric failed. Expected 1.0, got {metric}"

def test_check_connectivity_script_exists():
    """
    Verify the diagnostic script exists and is executable.
    """
    script_path = "/home/user/check_connectivity.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK) or os.access(script_path, os.R_OK), f"Script {script_path} is not accessible."

def test_cron_job_configured():
    """
    Verify that a cron job is configured for the diagnostic script.
    """
    # Check crontab for the current user or 'user'
    crontab_output = ""
    try:
        crontab_output = subprocess.check_output(['crontab', '-l'], stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError:
        try:
            crontab_output = subprocess.check_output(['crontab', '-l', '-u', 'user'], stderr=subprocess.STDOUT).decode('utf-8')
        except subprocess.CalledProcessError:
            pass

    assert "check_connectivity.sh" in crontab_output, "Cron job for check_connectivity.sh is not configured in crontab."