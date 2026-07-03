# test_final_state.py

import os
import socket
import subprocess
import pytest

def test_repositories_and_directories_exist():
    assert os.path.exists("/home/user/edge-update.git"), "Bare repository /home/user/edge-update.git does not exist."
    assert os.path.exists("/home/user/deployed"), "Deployment directory /home/user/deployed does not exist."
    assert os.path.exists("/home/user/source-repo"), "Source repository /home/user/source-repo does not exist."
    assert os.path.exists("/home/user/edge-update.git/hooks/post-receive"), "post-receive hook does not exist."
    assert os.path.exists("/home/user/deployed/monitor"), "Compiled monitor executable does not exist in deployed directory."

def test_deploy_log():
    log_path = "/home/user/deploy.log"
    assert os.path.exists(log_path), "/home/user/deploy.log does not exist."

    # Get latest commit hash from source repo
    try:
        result = subprocess.run(
            ["git", "-C", "/home/user/source-repo", "rev-parse", "main"],
            capture_output=True, text=True, check=True
        )
        latest_commit = result.stdout.strip()
    except subprocess.CalledProcessError:
        pytest.fail("Could not retrieve commit hash from /home/user/source-repo.")

    expected_log = f"DEPLOYED: {latest_commit}"
    with open(log_path, "r") as f:
        log_content = f.read()

    assert expected_log in log_content, f"Expected string '{expected_log}' not found in {log_path}."

def test_monitor_process_running():
    pid_file = "/home/user/monitor.pid"
    assert os.path.exists(pid_file), f"{pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer."
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} (from {pid_file}) is not running.")

def test_tcp_ping_pong():
    host = '127.0.0.1'
    port = 9090

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect((host, port))
            s.sendall(b"PING\n")
            response = s.recv(1024).decode('utf-8')
            assert response == "PONG\n", f"Expected 'PONG\\n', received {repr(response)}"
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused on {host}:{port}. The monitor daemon is not listening.")
    except socket.timeout:
        pytest.fail(f"Connection timed out when trying to read from {host}:{port}.")
    except Exception as e:
        pytest.fail(f"Unexpected error when communicating with monitor daemon: {e}")