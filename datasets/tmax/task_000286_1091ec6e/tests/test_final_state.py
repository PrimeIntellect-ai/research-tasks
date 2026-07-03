# test_final_state.py
import os
import subprocess
import time
import requests
import pytest

def test_health_status_file():
    health_file = "/home/user/data/health.status"
    assert os.path.isfile(health_file), f"Health status file {health_file} does not exist."
    with open(health_file, "r") as f:
        content = f.read().strip()
    assert content == "OK", f"Expected health.status to contain 'OK', found '{content}'"

def test_tz_server_binary():
    binary_path = "/app/tz-server-1.0/tz-server"
    assert os.path.isfile(binary_path), f"tz-server binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"tz-server binary at {binary_path} is not executable"

def get_pids_for_cmd(cmd_substring):
    try:
        output = subprocess.check_output(["pgrep", "-f", cmd_substring], text=True)
        return [int(pid) for pid in output.strip().split("\n") if pid]
    except subprocess.CalledProcessError:
        return []

def test_tz_server_processes():
    pids_8081 = get_pids_for_cmd(r"tz-server.*8081")
    assert pids_8081, "tz-server is not running on port 8081"

    pids_8082 = get_pids_for_cmd(r"tz-server.*8082")
    assert pids_8082, "tz-server is not running on port 8082"

    # Check timezone environment variable for at least one process of each
    for pids, port in [(pids_8081, 8081), (pids_8082, 8082)]:
        tz_found = False
        for pid in pids:
            try:
                with open(f"/proc/{pid}/environ", "rb") as f:
                    env_data = f.read().split(b'\0')
                    if b"TZ=Europe/Berlin" in env_data:
                        tz_found = True
                        break
            except Exception:
                pass
        assert tz_found, f"tz-server on port {port} is not running with TZ=Europe/Berlin"

def test_monitor_script_running():
    pids = get_pids_for_cmd("monitor.sh")
    assert pids, "monitor.sh is not running in the background"

def test_nginx_running():
    pids = get_pids_for_cmd("nginx")
    assert pids, "nginx is not running"

def test_nginx_endpoints():
    # Test /time endpoint multiple times to ensure load balancing works and both upstream servers respond
    time_url = "http://127.0.0.1:8080/time"
    for i in range(4):
        try:
            resp = requests.get(time_url, timeout=2)
            assert resp.status_code == 200, f"Expected HTTP 200 from {time_url}, got {resp.status_code}"
            assert "Europe/Berlin" in resp.text, f"Response from {time_url} did not contain 'Europe/Berlin': {resp.text}"
        except requests.RequestException as e:
            pytest.fail(f"Request to {time_url} failed: {e}")

    # Test /health endpoint
    health_url = "http://127.0.0.1:8080/health"
    try:
        resp = requests.get(health_url, timeout=2)
        assert resp.status_code == 200, f"Expected HTTP 200 from {health_url}, got {resp.status_code}"
        assert resp.text.strip() == "OK", f"Expected 'OK' from {health_url}, got '{resp.text}'"
    except requests.RequestException as e:
        pytest.fail(f"Request to {health_url} failed: {e}")