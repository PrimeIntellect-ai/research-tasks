# test_final_state.py

import os
import subprocess
import urllib.request
import time
import pytest

def test_deploy_script_executable():
    script_path = '/home/user/deploy.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_blocked_ips():
    file_path = '/home/user/blocked_ips.txt'
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip().splitlines()

    expected = [
        "192.168.1.50 4",
        "10.0.0.5 3",
        "10.10.10.10 2"
    ]
    assert content == expected, f"Content of {file_path} is incorrect. Expected top 3 IPs sorted by count."

def test_firewall_conf():
    file_path = '/home/user/firewall.conf'
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip().splitlines()

    expected = [
        "DENY_IP 192.168.1.50",
        "DENY_IP 10.0.0.5",
        "DENY_IP 10.10.10.10"
    ]
    assert content == expected, f"Content of {file_path} is incorrect. Expected DENY_IP lines matching blocked IPs."

def test_http_endpoint():
    url = "http://127.0.0.1:9090/"
    try:
        req = urllib.request.urlopen(url, timeout=5)
        body = req.read().decode('utf-8').strip()
        status = req.getcode()
    except Exception as e:
        pytest.fail(f"Failed to connect to {url}. Is the app running and socat forwarding correctly? Error: {e}")

    assert status == 200, f"Expected HTTP status 200, got {status}."
    assert body == "Deploy Success", f"Expected response body 'Deploy Success', got '{body}'."

def test_idempotency():
    script_path = '/home/user/deploy.sh'

    # Run the script a second time to test idempotency
    try:
        subprocess.run([script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running {script_path} a second time failed with error: {e.stderr.decode()}")

    time.sleep(1) # Allow background processes to settle

    # Check processes listening on ports
    try:
        ss_out = subprocess.check_output(['ss', '-lptn']).decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to run ss command: {e}")

    port_8080_count = sum(1 for line in ss_out.splitlines() if ':8080 ' in line)
    port_9090_count = sum(1 for line in ss_out.splitlines() if ':9090 ' in line)

    assert port_8080_count == 1, f"Expected exactly 1 process listening on 8080, found {port_8080_count}. Idempotency failed."
    assert port_9090_count == 1, f"Expected exactly 1 process listening on 9090, found {port_9090_count}. Idempotency failed."

    # Check socat process count specifically
    try:
        ps_out = subprocess.check_output(['ps', 'aux']).decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to run ps command: {e}")

    socat_9090_count = sum(1 for line in ps_out.splitlines() if 'socat' in line and '9090' in line and 'grep' not in line)
    assert socat_9090_count == 1, f"Expected exactly 1 socat process for 9090, found {socat_9090_count}. Idempotency failed."