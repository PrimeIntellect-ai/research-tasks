# test_final_state.py

import os
import time
import socket
import subprocess
import requests
import pytest

def check_http_proxy():
    try:
        response = requests.get("http://127.0.0.1:8080/legacy-status", timeout=2)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        assert response.text == "MIGRATION_AUTH_9921_ACCEPTED", f"Unexpected response body: {response.text}"
    except requests.RequestException as e:
        pytest.fail(f"HTTP proxy request failed: {e}")

def check_tcp_healthcheck():
    try:
        with socket.create_connection(("127.0.0.1", 8081), timeout=2) as s:
            data = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                data += chunk
            assert data == b"HEALTHY\n", f"Unexpected TCP response: {data}"
    except Exception as e:
        pytest.fail(f"TCP healthcheck failed: {e}")

def get_pids(pattern):
    try:
        output = subprocess.check_output(["pgrep", "-f", pattern], text=True)
        return [int(pid) for pid in output.strip().split()]
    except subprocess.CalledProcessError:
        return []

def test_services_running():
    """Test that the HTTP proxy and TCP healthcheck are functional."""
    check_http_proxy()
    check_tcp_healthcheck()

def test_supervision_resilience():
    """Test that the supervisor restarts killed processes."""
    legacy_pids = get_pids("/app/legacy_api")
    proxy_pids = get_pids("/home/user/proxy")

    assert legacy_pids, "legacy_api is not running"
    assert proxy_pids, "proxy is not running"

    # Kill the processes
    for pid in legacy_pids + proxy_pids:
        try:
            os.kill(pid, 9)
        except OSError:
            pass

    # Wait for the supervisor to restart them
    time.sleep(3)

    # Check if they are back up
    new_legacy_pids = get_pids("/app/legacy_api")
    new_proxy_pids = get_pids("/home/user/proxy")

    assert new_legacy_pids, "legacy_api was not restarted by the supervisor"
    assert new_proxy_pids, "proxy was not restarted by the supervisor"

    # Verify the services still work
    check_http_proxy()
    check_tcp_healthcheck()

def test_quota_management():
    """Test that the log file is truncated when it exceeds 500 KB."""
    log_file = "/home/user/logs/app.log"

    # Ensure directory and file exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Append 600 KB of garbage data
    with open(log_file, "ab") as f:
        f.write(os.urandom(600 * 1024))

    # Wait for the background loop to check and truncate
    time.sleep(4)

    # Check the size
    if os.path.exists(log_file):
        size = os.path.getsize(log_file)
        assert size < 50 * 1024, f"Log file was not truncated, size is {size} bytes"
    else:
        # If it was deleted instead of truncated, that's also acceptable, though truncation is requested.
        pass