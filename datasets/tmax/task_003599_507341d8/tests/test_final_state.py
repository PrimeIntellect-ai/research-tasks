# test_final_state.py

import os
import time
import socket
import requests
import pytest
import subprocess

BASE_URL = "http://127.0.0.1:8080"

def get_service_pid():
    try:
        output = subprocess.check_output(["ss", "-lptn"], text=True)
        for line in output.splitlines():
            if ":8080" in line and "LISTEN" in line:
                # Extract PID from string like users:(("aggregator",pid=1234,fd=3))
                parts = line.split("pid=")
                if len(parts) > 1:
                    return int(parts[1].split(",")[0])
    except Exception:
        pass
    return None

def test_health_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/health: {e}")

def test_aggregate_precision():
    payload = {"values": [10000.0, 3.14159, -10000.0]}
    try:
        response = requests.post(f"{BASE_URL}/aggregate", json=payload, timeout=2)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
        data = response.json()
        assert "result" in data, "Response JSON missing 'result' key"

        # Expected result is exactly 3.14159 if precision is handled correctly (f64 or Kahan)
        # Naive f32 sum would likely give something like 3.14160156 or similar due to catastrophic cancellation.
        result = data["result"]
        assert abs(result - 3.14159) < 1e-9, f"Precision issue detected. Expected ~3.14159, got {result}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/aggregate: {e}")

def test_cancellation_leak():
    pid = get_service_pid()
    assert pid is not None, "Could not find PID of the service listening on 8080"

    def get_memory_kb():
        with open(f"/proc/{pid}/status", "r") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1])
        return 0

    initial_memory = get_memory_kb()

    # Simulate multiple aborted requests
    for _ in range(50):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect(("127.0.0.1", 8080))
            # Send partial request
            request = b"POST /aggregate HTTP/1.1\r\nHost: 127.0.0.1:8080\r\nContent-Length: 100000\r\n\r\n{\"values\": [1.0, "
            s.sendall(request)
            # Forcefully close the socket to simulate client disconnect
            s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, b'\x01\x00\x00\x00\x00\x00\x00\x00')
            s.close()
        except Exception:
            pass

    # Give the service a moment to clean up (or leak)
    time.sleep(2)

    final_memory = get_memory_kb()

    # If it leaks, memory will grow significantly. 50 requests with 100k content length could leak a few MBs.
    # We allow some small tolerance for normal memory allocator behavior.
    memory_growth = final_memory - initial_memory
    assert memory_growth < 5000, f"Memory leak detected! VmRSS grew by {memory_growth} KB after aborted requests."

    # Ensure service is still responsive
    test_health_endpoint()