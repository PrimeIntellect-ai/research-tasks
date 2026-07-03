# test_final_state.py

import os
import stat
import subprocess
import requests
import pytest
import time

def test_files_exist_and_permissions():
    # Check Makefile
    assert os.path.isfile('/home/user/src/Makefile'), "Makefile is missing at /home/user/src/Makefile"

    # Check metric_server executable
    server_path = '/home/user/bin/metric_server'
    assert os.path.isfile(server_path), f"Executable missing at {server_path}"
    assert os.access(server_path, os.X_OK), f"{server_path} is not executable"

    # Check watchdog.sh executable
    watchdog_path = '/home/user/bin/watchdog.sh'
    assert os.path.isfile(watchdog_path), f"Watchdog script missing at {watchdog_path}"
    assert os.access(watchdog_path, os.X_OK), f"{watchdog_path} is not executable"

def test_crontab():
    try:
        output = subprocess.check_output(['crontab', '-l'], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Is it configured?")

    # Simple check for the watchdog script in crontab
    # Looking for a 1-minute cron syntax, typically * * * * *
    lines = [line.strip() for line in output.split('\n') if line.strip() and not line.strip().startswith('#')]
    found = False
    for line in lines:
        if '/home/user/bin/watchdog.sh' in line:
            parts = line.split()
            if len(parts) >= 6 and parts[:5] == ['*', '*', '*', '*', '*']:
                found = True
                break
    assert found, "Crontab does not contain a 1-minute cron entry for /home/user/bin/watchdog.sh"

def test_http_server_responses():
    base_url = "http://127.0.0.1:8085/status"
    token = "secr3t-auth-77X"

    # Test 1: Valid token
    try:
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(base_url, headers=headers, timeout=5)
        assert r.status_code == 200, f"Expected 200 OK with valid token, got {r.status_code}"
        assert r.text == "OK\n", f"Expected body 'OK\\n', got {repr(r.text)}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to metric_server: {e}")

    # Test 2: Missing token
    try:
        r = requests.get(base_url, timeout=5)
        assert r.status_code == 401, f"Expected 401 Unauthorized without token, got {r.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to metric_server: {e}")

    # Test 3: Wrong token
    try:
        headers = {"Authorization": "Bearer wrong-token"}
        r = requests.get(base_url, headers=headers, timeout=5)
        assert r.status_code == 401, f"Expected 401 Unauthorized with wrong token, got {r.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to metric_server: {e}")