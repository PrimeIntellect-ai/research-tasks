# test_final_state.py

import os
import stat
import urllib.request
import pytest

def test_success_txt_exists_and_content():
    success_path = "/home/user/restore/success.txt"
    assert os.path.isfile(success_path), f"File {success_path} is missing. Did you save the curl output?"

    with open(success_path, "r") as f:
        content = f.read().strip()

    assert content == "ANALYTICS_RESTORE", f"Expected 'ANALYTICS_RESTORE' in success.txt, but got '{content}'."

def test_backend_sock_exists_and_is_socket():
    sock_path = "/home/user/restore/run/backend.sock"
    assert os.path.exists(sock_path), f"Socket file {sock_path} is missing."

    mode = os.stat(sock_path).st_mode
    assert stat.S_ISSOCK(mode), f"File {sock_path} exists but is not a socket."

def test_backend_pid_file_and_process_running():
    pid_path = "/home/user/restore/run/backend.pid"
    assert os.path.isfile(pid_path), f"PID file {pid_path} is missing."

    with open(pid_path, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_path} does not contain a valid integer PID."
    pid = int(pid_str)

    # Check if process is running
    proc_dir = f"/proc/{pid}"
    assert os.path.isdir(proc_dir), f"Process with PID {pid} (from {pid_path}) is not running."

    # Check if it's the backend process
    with open(f"{proc_dir}/cmdline", "r") as f:
        cmdline = f.read().replace('\0', ' ')

    assert "backend" in cmdline, f"Process {pid} is running, but it doesn't appear to be the backend process. Cmdline: {cmdline}"

def test_nginx_running():
    # Check if nginx is running by looking through /proc
    nginx_running = False
    for pid in os.listdir('/proc'):
        if pid.isdigit():
            try:
                with open(f"/proc/{pid}/cmdline", "r") as f:
                    cmdline = f.read().replace('\0', ' ')
                    if "nginx" in cmdline and "master process" in cmdline:
                        nginx_running = True
                        break
            except Exception:
                pass

    assert nginx_running, "Nginx master process is not running."

def test_nginx_responds_correctly():
    # Verify the actual service is working as requested
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/api")
        with urllib.request.urlopen(req, timeout=2) as response:
            body = response.read().decode('utf-8').strip()
            assert body == "ANALYTICS_RESTORE", f"Nginx returned unexpected body: {body}"
    except Exception as e:
        pytest.fail(f"Failed to fetch from Nginx on http://127.0.0.1:8080/api: {e}")