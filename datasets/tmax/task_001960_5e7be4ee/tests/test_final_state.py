# test_final_state.py

import os
import socket
import random
import time
import subprocess
import pytest
import psutil

def test_poly_solver_executable():
    solver_path = "/app/poly_solver"
    assert os.path.isfile(solver_path), f"Expected file {solver_path} does not exist."
    assert os.access(solver_path, os.X_OK), f"File {solver_path} is not executable. The environment issue was not fixed."

def test_server_memory_leak():
    server_path = "/home/user/poly_service/server.py"
    assert os.path.isfile(server_path), f"Expected file {server_path} does not exist."

    # Start the server
    proc = subprocess.Popen(["python", server_path])

    # Wait for the server to start and bind to the socket
    time.sleep(2)

    assert proc.poll() is None, "The server process terminated unexpectedly. Check if it binds to /tmp/poly.sock successfully."

    sock_path = "/tmp/poly.sock"
    assert os.path.exists(sock_path), f"Socket {sock_path} does not exist."

    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(sock_path)
    except Exception as e:
        proc.terminate()
        pytest.fail(f"Failed to connect to socket {sock_path}: {e}")

    try:
        for _ in range(10000):
            coeffs = " ".join(str(random.uniform(-10, 10)) for _ in range(5))
            client.sendall(coeffs.encode() + b"\n")
            # We must receive the response to ensure the server processes it
            client.recv(1024)

        p = psutil.Process(proc.pid)
        peak_rss_mb = p.memory_info().rss / (1024 * 1024)
    finally:
        client.close()
        proc.terminate()
        proc.wait(timeout=5)

    threshold = 50.0
    assert peak_rss_mb <= threshold, f"Memory leak detected! Peak RSS was {peak_rss_mb:.2f} MB, which is greater than the threshold of {threshold} MB."