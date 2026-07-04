# test_final_state.py

import os
import socket
import pytest

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def test_files_exist_and_permissions():
    """Check that launch.sh and monitor.c exist, and launch.sh is executable with set -e."""
    launch_sh = "/home/user/launch.sh"
    monitor_c = "/home/user/monitor.c"

    assert os.path.isfile(launch_sh), f"{launch_sh} does not exist."
    assert os.path.isfile(monitor_c), f"{monitor_c} does not exist."

    # Check executable bit
    assert os.access(launch_sh, os.X_OK), f"{launch_sh} is not executable."

    # Check set -e
    with open(launch_sh, 'r') as f:
        content = f.read()
    assert "set -e" in content, f"{launch_sh} must use 'set -e' for error handling."

def test_monitor_c_headers():
    """Check that monitor.c contains socket programming includes."""
    monitor_c = "/home/user/monitor.c"
    with open(monitor_c, 'r') as f:
        content = f.read()

    assert "sys/socket.h" in content, f"{monitor_c} does not include <sys/socket.h>."
    assert "arpa/inet.h" in content or "netinet/in.h" in content, f"{monitor_c} does not include <arpa/inet.h> or <netinet/in.h>."

def test_port_9001_running():
    """Check that port 9001 is actively listening."""
    assert is_port_in_use(9001), "Port 9001 is not listening. The server should be running."

def test_port_9002_not_running():
    """Check that port 9002 is not listening."""
    assert not is_port_in_use(9002), "Port 9002 is listening. The server should have been killed."

def test_monitor_log():
    """Check that monitor.log contains exactly the expected alert."""
    log_file = "/home/user/monitor.log"
    assert os.path.isfile(log_file), f"{log_file} does not exist."

    with open(log_file, 'r') as f:
        content = f.read()

    expected = "ALERT: PORT 9002 DOWN\n"
    assert content == expected, f"{log_file} content is incorrect. Expected {repr(expected)}, got {repr(content)}"