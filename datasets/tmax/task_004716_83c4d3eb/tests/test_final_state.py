# test_final_state.py

import os
import socket
import time
import subprocess
import requests
import pytest

def test_bisection_result():
    """Verify that the correct commit hash was found and written to the result file."""
    bisection_file = "/home/user/bisection_result.txt"
    assert os.path.exists(bisection_file), f"{bisection_file} does not exist"

    # Find the expected commit hash from the git log
    result = subprocess.run(
        ["git", "log", "--grep=Optimize parsing with zero-copy slice indexing", "--format=%H"],
        cwd="/app/telemetry_ingester",
        capture_output=True,
        text=True
    )
    expected_hash = result.stdout.strip()
    assert expected_hash, "Could not find the expected commit in the git repository."

    with open(bisection_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Bisection result is incorrect. Expected {expected_hash}, got {actual_hash}"

def test_services_running():
    """Ensure Redis, Rust Ingester, and Python API are listening on their respective ports."""
    ports = {
        6379: "Redis",
        8080: "Telemetry Ingester (Rust)",
        9090: "Telemetry API (Python)"
    }

    for port, service in ports.items():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            result = s.connect_ex(("127.0.0.1", port))
            assert result == 0, f"{service} is not listening on port {port}"

def test_ingester_resilience_and_functionality():
    """
    Send a malformed payload to the Rust ingester, verify it doesn't crash,
    then send a valid payload and verify it appears in the API.
    """
    # 1. Send malformed packet (length 16, but only 5 bytes of data)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect(("127.0.0.1", 8080))
            s.sendall(b"\x00\x10short")
    except Exception:
        # It is acceptable for the connection to be closed by the server
        pass

    # Wait briefly to see if the process crashes
    time.sleep(1)

    # 2. Ensure port 8080 is still open (process did not panic)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex(("127.0.0.1", 8080))
        assert result == 0, "Telemetry Ingester crashed (port 8080 closed) after receiving a malformed packet."

    # 3. Send valid packet (length 5, 5 bytes of data)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect(("127.0.0.1", 8080))
            s.sendall(b"\x00\x05hello")
    except Exception as e:
        pytest.fail(f"Failed to send valid packet to Ingester: {e}")

    # Wait briefly for the ingester to process and push to Redis
    time.sleep(1)

    # 4. Check the API for the valid payload
    try:
        resp = requests.get("http://127.0.0.1:9090/metrics", timeout=2)
        assert resp.status_code == 200, f"API returned status code {resp.status_code}"
        data = resp.json()
    except Exception as e:
        pytest.fail(f"Failed to query Telemetry API: {e}")

    # Verify that the payload "hello" made it through the system
    assert "hello" in str(data), f"Valid payload 'hello' was not found in the API response. Actual response: {data}"