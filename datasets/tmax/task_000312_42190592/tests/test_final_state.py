# test_final_state.py

import os
import stat
import socket
import subprocess
import requests
import pytest

# Expected passcode based on "delta seven seven"
PASSCODE = "DELTA77"

def test_provision_script_idempotent():
    path = "/home/user/provision.py"
    assert os.path.isfile(path), f"Provisioning script missing at {path}"

    # Run the script again to verify idempotency
    result = subprocess.run(["python3", path], capture_output=True, text=True)
    assert result.returncode == 0, f"Provisioning script failed on second run: {result.stderr}"

def test_directory_and_file_permissions():
    log_dir = "/home/user/app_logs/"
    log_file = "/home/user/app_logs/auth.log"

    assert os.path.isdir(log_dir), f"Log directory missing at {log_dir}"
    dir_stat = os.stat(log_dir)
    assert stat.S_IMODE(dir_stat.st_mode) == 0o700, f"Log directory permissions incorrect: {oct(dir_stat.st_mode)}"

    assert os.path.isfile(log_file), f"Log file missing at {log_file}"
    file_stat = os.stat(log_file)
    assert stat.S_IMODE(file_stat.st_mode) == 0o600, f"Log file permissions incorrect: {oct(file_stat.st_mode)}"

def test_logrotate_config():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"logrotate.conf missing at {conf_path}"

    # Run logrotate with the config to ensure it's valid
    result = subprocess.run(["logrotate", "-d", conf_path], capture_output=True, text=True)
    assert result.returncode == 0, f"logrotate configuration is invalid: {result.stderr}"

def test_http_over_ssh_tunnel():
    # Test successful request
    headers = {"X-Auth-Passcode": PASSCODE}
    try:
        response = requests.get("http://127.0.0.1:9999/", headers=headers, timeout=5)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
        assert response.text.strip() == "ACCESS_GRANTED", f"Expected 'ACCESS_GRANTED', got '{response.text}'"
    except requests.RequestException as e:
        pytest.fail(f"HTTP request over SSH tunnel failed: {e}")

    # Test forbidden request
    try:
        response = requests.get("http://127.0.0.1:9999/", timeout=5)
        assert response.status_code == 403, f"Expected HTTP 403, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"HTTP request over SSH tunnel failed: {e}")

def test_raw_tcp_component():
    # Test successful request
    try:
        with socket.create_connection(("127.0.0.1", 8889), timeout=5) as s:
            s.sendall(f"{PASSCODE}\n".encode("utf-8"))
            response = s.recv(1024).decode("utf-8")
            assert response.strip() == "ACCESS_GRANTED", f"Expected 'ACCESS_GRANTED', got '{response}'"
    except (socket.error, socket.timeout) as e:
        pytest.fail(f"TCP connection failed: {e}")

    # Test denied request
    try:
        with socket.create_connection(("127.0.0.1", 8889), timeout=5) as s:
            s.sendall(b"WRONGPASS\n")
            response = s.recv(1024).decode("utf-8")
            assert response.strip() == "DENIED", f"Expected 'DENIED', got '{response}'"
    except (socket.error, socket.timeout) as e:
        pytest.fail(f"TCP connection failed: {e}")

def test_logging_behavior():
    log_file = "/home/user/app_logs/auth.log"
    assert os.path.isfile(log_file), f"Log file missing at {log_file}"

    with open(log_file, "r") as f:
        content = f.read()

    # Check for HTTP and TCP log entries
    assert "[HTTP]" in content, "Missing [HTTP] log entries"
    assert "[TCP]" in content, "Missing [TCP] log entries"