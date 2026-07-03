# test_final_state.py

import os
import socket
import subprocess
import time
import pytest

def test_start_service_script_exists():
    script_path = "/app/legacy_proc/start_service.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing"
    assert os.access(script_path, os.X_OK), f"Script {script_path} must be executable"

def test_benchmark_script_exists():
    script_path = "/app/legacy_proc/benchmark.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing"
    assert os.access(script_path, os.X_OK), f"Script {script_path} must be executable"

def test_start_service_script_contents():
    script_path = "/app/legacy_proc/start_service.sh"
    with open(script_path, "r") as f:
        content = f.read()

    assert "0x7F4A" in content, "The start_service.sh script does not contain the extracted ABI magic value (0x7F4A)."
    assert "MATRIX_ABI_MAGIC" in content, "The start_service.sh script does not export MATRIX_ABI_MAGIC."
    assert "v2" in content, "The start_service.sh script does not seem to set the library path to the v2 directory."

def test_tcp_service_responds():
    script_path = "/app/legacy_proc/start_service.sh"

    # Start the service
    proc = subprocess.Popen([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the service to bind to the port
    port = 9099
    connected = False
    for _ in range(20):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                connected = True
                break
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(0.5)

    if not connected:
        proc.terminate()
        pytest.fail(f"Could not connect to service on port {port} after running {script_path}")

    try:
        with socket.create_connection(("127.0.0.1", port), timeout=2) as s:
            s.sendall(b"INPUT_MATRIX_44\n")
            response = s.recv(4096)
            assert len(response) > 0, "The service did not return any data. The binary might have crashed due to incorrect environment variables."
    finally:
        proc.terminate()
        proc.wait(timeout=2)