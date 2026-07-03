# test_final_state.py
import os
import json
import time
import subprocess
import urllib.request
import urllib.error
import pytest

RCA_FILE = "/home/user/rca.json"
START_SCRIPT = "/home/user/services/start.sh"
FRONTEND_URL = "http://127.0.0.1:8080"

def test_rca_json_exists_and_valid():
    assert os.path.isfile(RCA_FILE), f"RCA file {RCA_FILE} does not exist."
    with open(RCA_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"RCA file {RCA_FILE} is not valid JSON.")

    assert "failing_component" in data, "Missing 'failing_component' in RCA."
    assert data["failing_component"] == "backend", "Incorrect failing_component."

    assert "failing_syscall" in data, "Missing 'failing_syscall' in RCA."
    assert data["failing_syscall"] in ["openat", "open"], "Incorrect failing_syscall."

    assert "errno" in data, "Missing 'errno' in RCA."
    assert data["errno"] == "EMFILE", "Incorrect errno."

def is_service_running(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=1) as response:
            return response.status == 200
    except Exception:
        return False

def test_backend_fix_under_load():
    # Ensure services are running
    if not is_service_running(FRONTEND_URL):
        subprocess.run([START_SCRIPT], check=True)
        # Wait for services to be up
        for _ in range(10):
            if is_service_running(FRONTEND_URL):
                break
            time.sleep(1)
        else:
            pytest.fail("Services failed to start or become healthy.")

    # Send 1500 requests to trigger the leak if it still exists
    success_count = 0
    bad_gateway_count = 0
    error_count = 0

    for i in range(1500):
        try:
            req = urllib.request.Request(FRONTEND_URL)
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    success_count += 1
                else:
                    error_count += 1
        except urllib.error.HTTPError as e:
            if e.code == 502:
                bad_gateway_count += 1
            else:
                error_count += 1
        except Exception:
            error_count += 1

    assert bad_gateway_count == 0, f"Received {bad_gateway_count} '502 Bad Gateway' responses. The file descriptor leak is likely not fixed."
    assert success_count > 0, "No successful requests were made to the frontend."