# test_final_state.py

import os
import socket
import subprocess
import pytest

def test_healthd_compiled():
    executable_path = "/home/user/healthd"
    assert os.path.isfile(executable_path), f"Executable {executable_path} not found."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_worker_running():
    pid_file = "/home/user/worker.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} not found."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: '{pid_str}'"

    pid = int(pid_str)
    assert os.path.isdir(f"/proc/{pid}"), f"Worker process with PID {pid} is not running."

def test_daemon_listening_and_response():
    try:
        with socket.create_connection(("127.0.0.1", 8080), timeout=2) as s:
            response = s.recv(1024).decode("utf-8").strip()
    except ConnectionRefusedError:
        pytest.fail("Daemon is not listening on 127.0.0.1:8080")
    except socket.timeout:
        pytest.fail("Daemon connection timed out on 127.0.0.1:8080")
    except Exception as e:
        pytest.fail(f"Failed to connect or read from daemon: {e}")

    assert "STATUS: OK" in response, f"Expected 'STATUS: OK' in response, got '{response}'"

def test_crontab_updated():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab.")

    assert "LOG_DIR=/home/user/logs" in crontab_content, "Crontab does not contain 'LOG_DIR=/home/user/logs'"
    assert "/home/user/query_health.sh" in crontab_content, "Crontab does not contain the query_health.sh script"

def test_log_file_populated():
    log_file = "/home/user/logs/status.log"
    assert os.path.isfile(log_file), f"Log file {log_file} not found."

    with open(log_file, "r") as f:
        content = f.read()

    assert "STATUS: OK" in content, f"Log file {log_file} does not contain 'STATUS: OK'"