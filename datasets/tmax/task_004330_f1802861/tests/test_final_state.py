# test_final_state.py
import os
import sys
import subprocess
import time
import requests
import pytest

def get_process_rss(pid):
    """Return the RSS memory of the given PID in kilobytes."""
    with open(f"/proc/{pid}/status", "r") as f:
        for line in f:
            if line.startswith("VmRSS:"):
                return int(line.split()[1])
    return 0

def get_server_pid(port):
    """Find the PID of the process listening on the given port."""
    try:
        output = subprocess.check_output(["ss", "-lptn"], stderr=subprocess.DEVNULL).decode()
        for line in output.splitlines():
            if f":{port}" in line and "LISTEN" in line:
                # Extract pid from something like users:(("python3",pid=1234,fd=3))
                parts = line.split("pid=")
                if len(parts) > 1:
                    return int(parts[1].split(",")[0])
    except Exception:
        pass
    return None

def test_mre_exists_and_runs():
    mre_path = "/home/user/mre.py"
    assert os.path.isfile(mre_path), f"MRE script missing at {mre_path}"

    # Run the MRE script and ensure it exits with code 0
    result = subprocess.run([sys.executable, mre_path], capture_output=True, text=True)
    assert result.returncode == 0, f"MRE script failed to run. Stderr: {result.stderr}"

def test_server_running_and_correct():
    url = "http://127.0.0.1:8888/api/v1/diff"
    payload = {"base": {"key": "value1"}, "diff": {"key": "value2"}}

    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except Exception:
        pytest.fail(f"Failed to parse JSON response: {response.text}")

    assert data == {"key": "value2"}, f"Expected merged dictionary {{'key': 'value2'}}, got {data}"

def test_server_memory_leak_fixed():
    pid = get_server_pid(8888)
    assert pid is not None, "Could not find server process listening on port 8888"

    url = "http://127.0.0.1:8888/api/v1/diff"
    payload = {"base": {"key": "value1", "other": "data"}, "diff": {"key": "value2", "new": "data"}}

    # Warm up
    for _ in range(10):
        requests.post(url, json=payload)

    initial_rss = get_process_rss(pid)
    assert initial_rss > 0, "Could not read initial RSS memory"

    # Send 2000 requests
    for _ in range(2000):
        response = requests.post(url, json=payload)
        assert response.status_code == 200

    final_rss = get_process_rss(pid)

    # Check that memory hasn't grown by more than 5MB (5120 KB)
    growth = final_rss - initial_rss
    assert growth < 5120, f"Memory leak detected: RSS grew by {growth} KB (from {initial_rss} to {final_rss} KB)"