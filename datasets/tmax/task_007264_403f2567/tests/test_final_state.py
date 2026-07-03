# test_final_state.py

import os
import socket
import subprocess
import pytest

def test_app_users_txt():
    """Verify that app_users.txt exists and contains the correct access control line."""
    path = "/home/user/app_users.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "admin:network_engineers", f"Incorrect content in {path}. Expected 'admin:network_engineers', got '{content}'."

def test_apptainer_instance_running():
    """Verify that the Apptainer instance 'backend_svc' is running."""
    try:
        result = subprocess.run(["apptainer", "instance", "list"], capture_output=True, text=True, check=True)
        assert "backend_svc" in result.stdout, "Apptainer instance 'backend_svc' is not running."
    except FileNotFoundError:
        pytest.fail("apptainer command not found. Is it installed?")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to list apptainer instances: {e.stderr}")

def test_port_8080_forwarding():
    """Verify that port 8080 forwards to the backend service and can handle multiple connections."""
    # Connect twice to ensure the proxy handles multiple connections (e.g. socat fork)
    for i in range(2):
        try:
            with socket.create_connection(("127.0.0.1", 8080), timeout=2) as s:
                data = s.recv(1024).decode("utf-8", errors="ignore")
                assert "HELLO_FROM_BACKEND" in data, f"Connection {i+1}: Did not receive expected banner 'HELLO_FROM_BACKEND' from port 8080. Received: {data}"
        except Exception as e:
            pytest.fail(f"Connection {i+1}: Failed to connect and read from 127.0.0.1:8080: {e}")

def test_healthcheck_executable():
    """Verify that the healthcheck executable was compiled and exists."""
    path = "/home/user/healthcheck"
    assert os.path.exists(path), f"Executable {path} does not exist. Did you compile healthcheck.c?"
    assert os.access(path, os.X_OK), f"File {path} exists but is not executable."

def test_result_log():
    """Verify that result.log exists and contains the successful output from the healthcheck."""
    path = "/home/user/result.log"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "HELLO_FROM_BACKEND" in content, f"Expected 'HELLO_FROM_BACKEND' in {path}, but it was not found."