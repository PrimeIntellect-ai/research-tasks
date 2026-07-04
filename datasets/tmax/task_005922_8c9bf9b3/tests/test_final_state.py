# test_final_state.py

import os
import socket
import pytest

def test_backends_list_exists_and_content():
    """Verify /home/user/lb/backends.list exists and has the correct contents."""
    filepath = "/home/user/lb/backends.list"
    assert os.path.isfile(filepath), f"{filepath} does not exist."
    with open(filepath, "r") as f:
        content = f.read().strip()

    expected_content = (
        "server backend_A 127.0.0.1:8001\n"
        "server backend_B 127.0.0.1:8002\n"
        "server backend_C 127.0.0.1:8003"
    )
    assert content == expected_content, f"Contents of {filepath} do not match the expected setup."

def test_ports_listening():
    """Verify that ports 8001 and 8003 are listening, and 8002 is not."""
    def is_port_open(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(('127.0.0.1', port)) == 0

    assert is_port_open(8001), "Port 8001 is not listening (backend_A)."
    assert not is_port_open(8002), "Port 8002 is listening, but it should be dead (backend_B)."
    assert is_port_open(8003), "Port 8003 is not listening (backend_C)."

def test_monitor_script_executable():
    """Verify /home/user/lb/monitor.sh exists and is executable."""
    filepath = "/home/user/lb/monitor.sh"
    assert os.path.isfile(filepath), f"{filepath} does not exist."
    assert os.access(filepath, os.X_OK), f"{filepath} is not executable."

def test_active_list_content():
    """Verify /home/user/lb/active.list has the expected contents."""
    filepath = "/home/user/lb/active.list"
    assert os.path.isfile(filepath), f"{filepath} does not exist. Did you run the script?"
    with open(filepath, "r") as f:
        content = f.read().strip()

    expected_content = (
        "server backend_A 127.0.0.1:8001\n"
        "# server backend_B 127.0.0.1:8002\n"
        "server backend_C 127.0.0.1:8003"
    )
    assert content == expected_content, f"Contents of {filepath} do not match the expected output."

def test_health_log_content():
    """Verify /home/user/lb/health.log has the expected error string."""
    filepath = "/home/user/lb/health.log"
    assert os.path.isfile(filepath), f"{filepath} does not exist. Did you run the script?"
    with open(filepath, "r") as f:
        content = f.read().strip()

    expected_error = "ERROR: backend_B on 127.0.0.1:8002 is unreachable"
    assert expected_error in content, f"Expected error not found in {filepath}."