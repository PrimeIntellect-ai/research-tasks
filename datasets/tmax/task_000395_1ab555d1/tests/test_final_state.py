# test_final_state.py

import socket
import struct
import time
import json
import urllib.request
import pytest

def send_aborted_request(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((host, port))

        # Send a basic HTTP POST request
        request = b"POST /process HTTP/1.1\r\nHost: " + f"{host}:{port}".encode() + b"\r\nContent-Length: 0\r\n\r\n"
        s.sendall(request)

        # Force a TCP RST by setting SO_LINGER with 0 timeout
        l_onoff = 1
        l_linger = 0
        s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', l_onoff, l_linger))
        s.close()
    except Exception:
        pass

def test_no_task_leak_on_aborted_connections():
    host = '127.0.0.1'
    port = 8080

    # Verify the server is running and accessible
    try:
        req = urllib.request.Request(f"http://{host}:{port}/__stats__")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        pytest.fail(f"Could not connect to the service at http://{host}:{port}/__stats__ to get initial stats: {e}")

    initial_tasks = data.get("active_tasks", 0)

    # Simulate 1,000 aborted connections
    num_requests = 1000
    for _ in range(num_requests):
        send_aborted_request(host, port)

    # Give the server a moment to process the disconnects and clean up tasks
    time.sleep(2)

    # Query stats again
    try:
        req = urllib.request.Request(f"http://{host}:{port}/__stats__")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        pytest.fail(f"Could not connect to the service at http://{host}:{port}/__stats__ after load test: {e}")

    final_tasks = data.get("active_tasks", 0)

    # The threshold is <= 5 active tasks remaining
    # We account for the initial tasks just in case the server has a baseline
    leaked_tasks = final_tasks - initial_tasks

    assert leaked_tasks <= 5, (
        f"Metric threshold failed: Expected <= 5 leaked tasks after {num_requests} aborted connections, "
        f"but found {leaked_tasks} leaked tasks. (Initial: {initial_tasks}, Final: {final_tasks})"
    )