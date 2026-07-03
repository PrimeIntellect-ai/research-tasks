# test_final_state.py

import os
import time
import socket
import ssl
import urllib.request
import pytest

def test_supervisord_running():
    """Verify that supervisord is running and the PID file exists."""
    pid_file = "/home/user/supervisord.pid"
    assert os.path.isfile(pid_file), f"supervisord PID file not found at {pid_file}"

    with open(pid_file, 'r') as f:
        pid = f.read().strip()

    assert pid.isdigit(), "PID file does not contain a valid numeric PID"
    assert os.path.exists(f"/proc/{pid}"), f"supervisord process with PID {pid} is not running"

def test_ports_listening():
    """Verify that ports 8443 and 9090 are bound and listening."""
    def is_port_open(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(('127.0.0.1', port)) == 0

    assert is_port_open(8443), "Port 8443 (Python HTTPS server) is not accepting connections"
    assert is_port_open(9090), "Port 9090 (socat forwarder) is not accepting connections"

def test_end_to_end_alert():
    """Verify the C++ monitor detects a new .dat file and logs it, accessible via the forwarded port."""
    data_drop = "/home/user/data_drop"
    assert os.path.isdir(data_drop), f"Data drop directory {data_drop} does not exist"

    test_filename = "verification_test.dat"
    test_filepath = os.path.join(data_drop, test_filename)

    # Create the test file to trigger inotify
    with open(test_filepath, 'w') as f:
        f.write("test data")

    # Allow some time for the C++ monitor to process the event and flush to the log
    time.sleep(2)

    # Fetch the log via the socat forwarded port
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://127.0.0.1:9090/alerts.log"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to fetch alerts.log via {url}. Error: {e}")

    expected_log = '{"alert": "new_data", "file": "verification_test.dat"}'
    assert expected_log in content, (
        f"Expected log entry '{expected_log}' not found in alerts.log. "
        f"Actual content:\n{content}"
    )