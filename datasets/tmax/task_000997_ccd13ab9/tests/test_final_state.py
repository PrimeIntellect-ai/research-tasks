# test_final_state.py

import os
import time
import requests
import subprocess
import pytest

def test_binary_exists_and_executable():
    path = "/home/user/microserver_bin"
    assert os.path.isfile(path), f"Binary {path} does not exist. Did you compile and move it?"
    assert os.access(path, os.X_OK), f"Binary {path} is not executable."

def test_start_server_script_contents():
    path = "/home/user/start_server.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "TZ=Pacific/Auckland" in content or "TZ='Pacific/Auckland'" in content or 'TZ="Pacific/Auckland"' in content, "TZ is not set to Pacific/Auckland in start_server.sh"
    assert "LC_ALL=en_NZ.UTF-8" in content or "LC_ALL='en_NZ.UTF-8'" in content or 'LC_ALL="en_NZ.UTF-8"' in content, "LC_ALL is not set to en_NZ.UTF-8 in start_server.sh"

def test_socat_process_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "socat.*8080.*9090"], text=True)
        assert output.strip(), "socat process forwarding 8080 to 9090 is not running."
    except subprocess.CalledProcessError:
        pytest.fail("socat process forwarding 8080 to 9090 is not running.")

def test_microserver_process_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "microserver_bin.*9090"], text=True)
        assert output.strip(), "microserver_bin process is not running on port 9090."
    except subprocess.CalledProcessError:
        pytest.fail("microserver_bin process is not running on port 9090.")

def test_http_endpoints_via_socat():
    # Wait briefly in case it just started
    time.sleep(1)

    # 1. index.html
    try:
        r1 = requests.get("http://127.0.0.1:8080/index.html", timeout=2)
        assert r1.status_code == 200, f"Expected 200 OK for index.html, got {r1.status_code}"
        assert r1.text.strip() == "DEPLOYMENT_SUCCESS", f"Expected DEPLOYMENT_SUCCESS, got {r1.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to http://127.0.0.1:8080/index.html: {e}")

    # 2. data.txt
    try:
        r2 = requests.get("http://127.0.0.1:8080/data.txt", timeout=2)
        assert r2.status_code == 200, f"Expected 200 OK for data.txt, got {r2.status_code}"
        assert r2.text.strip() == "SENSITIVE_DATA", f"Expected SENSITIVE_DATA, got {r2.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to http://127.0.0.1:8080/data.txt: {e}")

    # 3. health
    try:
        r3 = requests.get("http://127.0.0.1:8080/health", timeout=2)
        assert r3.status_code == 200, f"Expected 200 OK for health, got {r3.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to http://127.0.0.1:8080/health: {e}")

def test_status_log_contains_up():
    path = "/home/user/status.log"
    # Wait a bit to ensure monitor script has run
    for _ in range(5):
        if os.path.isfile(path):
            with open(path, "r") as f:
                if f.read().strip() == "UP":
                    return
        time.sleep(1)

    assert os.path.isfile(path), f"Log file {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "UP", f"Expected status.log to contain 'UP', got '{content}'"