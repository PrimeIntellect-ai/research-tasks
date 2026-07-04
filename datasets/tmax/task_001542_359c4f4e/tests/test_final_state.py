# test_final_state.py
import os
import requests
import json
import time

def test_unlock_exp_exists():
    path = "/home/user/unlock.exp"
    assert os.path.isfile(path), f"Expect script {path} does not exist."

def test_fw_unlocked_flag():
    path = "/tmp/fw_unlocked"
    assert os.path.isfile(path), f"Firewall unlocked flag {path} does not exist. Did you run the expect script successfully?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "UNLOCKED", f"Expected 'UNLOCKED' in {path}, got '{content}'"

def test_monitor_service_c_exists():
    path = "/home/user/monitor_service.c"
    assert os.path.isfile(path), f"C source file {path} does not exist."

def test_monitor_service_binary_exists():
    path = "/home/user/monitor_service"
    assert os.path.isfile(path), f"Compiled binary {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_monitor_service_http_response():
    url = "http://127.0.0.1:8080/status"

    # Retry a few times in case the service is slow to start
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            break
        except requests.exceptions.RequestException as e:
            if i == max_retries - 1:
                assert False, f"Failed to connect to {url}: {e}"
            time.sleep(1)

    assert response.status_code == 200, f"Expected HTTP status 200, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {response.text}"

    assert data.get("status") == "UP", f"Expected status 'UP', got {data.get('status')}"
    assert data.get("auth") == "9428", f"Expected auth '9428', got {data.get('auth')}"