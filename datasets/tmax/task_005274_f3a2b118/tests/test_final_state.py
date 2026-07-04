# test_final_state.py

import os
import time
import json
import requests
import pytest
import subprocess

def test_patch_file_exists_and_contains_diffs():
    patch_path = "/home/user/py2num_migration.patch"
    assert os.path.exists(patch_path), f"Patch file missing at {patch_path}"

    with open(patch_path, "r") as f:
        content = f.read()

    # The patch should contain diffs for setup.py and core.py
    assert "setup.py" in content, "Patch file does not contain changes for setup.py"
    assert "core.py" in content, "Patch file does not contain changes for core.py"

def test_server_log_exists():
    log_path = "/home/user/server.log"
    assert os.path.exists(log_path), f"Server log missing at {log_path}"

def test_api_missing_auth():
    url = "http://127.0.0.1:8080/compute"
    payload = {"n": 10}
    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_api_invalid_payload():
    url = "http://127.0.0.1:8080/compute"
    headers = {"X-Migration-Auth": "99887766"}
    try:
        # Sending invalid JSON or missing 'n'
        response = requests.post(url, data="not a json", headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"

def test_api_valid_computations():
    url = "http://127.0.0.1:8080/compute"
    headers = {"X-Migration-Auth": "99887766"}

    # Test n=5
    try:
        resp1 = requests.post(url, json={"n": 5}, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp1.status_code == 200, f"Expected 200 OK, got {resp1.status_code}"
    data1 = resp1.json()
    assert data1.get("result") == 55, f"Expected result 55 for n=5, got {data1.get('result')}"

    # Test n=100
    try:
        resp2 = requests.post(url, json={"n": 100}, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp2.status_code == 200, f"Expected 200 OK, got {resp2.status_code}"
    data2 = resp2.json()
    assert data2.get("result") == 338350, f"Expected result 338350 for n=100, got {data2.get('result')}"

def get_server_pid():
    try:
        output = subprocess.check_output(["lsof", "-t", "-i:8080"], text=True)
        pids = output.strip().split('\n')
        if pids and pids[0]:
            return int(pids[0])
    except subprocess.CalledProcessError:
        pass
    return None

def get_memory_usage_mb(pid):
    status_file = f"/proc/{pid}/status"
    if not os.path.exists(status_file):
        return 0
    with open(status_file, "r") as f:
        for line in f:
            if line.startswith("VmRSS:"):
                # VmRSS: 12345 kB
                parts = line.split()
                if len(parts) >= 2:
                    kb = int(parts[1])
                    return kb / 1024.0
    return 0

def test_memory_leak_fixed():
    pid = get_server_pid()
    assert pid is not None, "Could not find server process listening on port 8080"

    url = "http://127.0.0.1:8080/compute"
    headers = {"X-Migration-Auth": "99887766"}

    # Send multiple large requests
    for _ in range(20):
        try:
            resp = requests.post(url, json={"n": 50000}, headers=headers, timeout=5)
            assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to server during memory test: {e}")

    # Check memory usage
    mem_mb = get_memory_usage_mb(pid)
    assert mem_mb < 100, f"Memory usage is too high: {mem_mb:.2f} MB. The memory leak might not be fixed."