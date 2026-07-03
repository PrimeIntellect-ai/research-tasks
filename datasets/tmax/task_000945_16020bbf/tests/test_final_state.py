# test_final_state.py
import os
import socket
import time
import subprocess
import pytest

def test_compiled_collector_exists():
    executable = '/home/user/bin/collector'
    assert os.path.isfile(executable), f"Compiled executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_logger_script_updated():
    script_path = '/app/logger.sh'
    assert os.path.isfile(script_path), f"Logger script {script_path} is missing."
    with open(script_path, 'r') as f:
        content = f.read()
    assert "PORT=9090" in content, "logger.sh was not updated to listen on port 9090."
    assert "PORT=9999" not in content, "logger.sh still contains the misconfigured port 9999."

def test_logrotate_config():
    config_path = '/home/user/config/logrotate.conf'
    assert os.path.isfile(config_path), f"Logrotate config {config_path} is missing."
    with open(config_path, 'r') as f:
        content = f.read()
    assert "/home/user/logs/capacity.log" in content, "Logrotate config missing target log file."
    assert "daily" in content, "Logrotate config missing 'daily' directive."
    assert "rotate 3" in content, "Logrotate config missing 'rotate 3' directive."

def test_collector_running_in_unshare():
    # Check if the process is running
    try:
        output = subprocess.check_output(['ps', '-eo', 'args']).decode('utf-8')
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps command.")

    assert "unshare -U -r /home/user/bin/collector" in output or "unshare -U -r" in output and "/home/user/bin/collector" in output, \
        "Collector is not running inside the required unshare user namespace."

def test_tcp_collector_response_and_logger_forwarding():
    host = '127.0.0.1'
    port = 8888
    message = b"CAPACITY_REPORT 500\n"

    # Send TCP request to collector
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((host, port))
            s.sendall(message)
            response = s.recv(1024)
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused to {host}:{port}. Is the collector running?")
    except socket.timeout:
        pytest.fail(f"Timeout waiting for response from collector on {host}:{port}.")
    except Exception as e:
        pytest.fail(f"Unexpected error communicating with collector: {e}")

    assert response == b"OK_RECORDED\n", f"Expected response 'OK_RECORDED\\n', but got {response!r}"

    # Wait a moment for UDP forwarding and log writing
    time.sleep(1)

    log_file = '/home/user/logs/capacity.log'
    assert os.path.isfile(log_file), f"Log file {log_file} was not created by the logger."

    with open(log_file, 'r') as f:
        log_content = f.read()

    assert "CAPACITY_REPORT 500" in log_content, "The logger did not record the forwarded capacity report."