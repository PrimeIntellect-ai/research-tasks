# test_final_state.py
import os
import stat
import urllib.request
import subprocess
import pytest

def get_expected_size():
    data_dir = "/home/user/data"
    total_size = 0
    if os.path.isdir(data_dir):
        for entry in os.listdir(data_dir):
            path = os.path.join(data_dir, entry)
            if os.path.isfile(path) and not os.path.islink(path):
                total_size += os.path.getsize(path)
    return total_size

def test_monitor_executable_exists():
    exe_path = "/home/user/bin/monitor"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable"

def test_socket_exists_and_is_socket():
    sock_path = "/home/user/run/app.sock"
    assert os.path.exists(sock_path), f"Socket {sock_path} does not exist"
    mode = os.stat(sock_path).st_mode
    assert stat.S_ISSOCK(mode), f"Path {sock_path} exists but is not a UNIX domain socket"

def test_result_log_content():
    log_path = "/home/user/result.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist"
    with open(log_path, "r") as f:
        content = f.read().strip()
    expected_size = get_expected_size()
    expected_str = f"USAGE: {expected_size}"
    assert content == expected_str, f"result.log content is incorrect. Expected '{expected_str}', got '{content}'"

def test_nginx_proxy_dynamic_response():
    expected_size = get_expected_size()
    expected_str = f"USAGE: {expected_size}"
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/status")
        with urllib.request.urlopen(req, timeout=2) as response:
            content = response.read().decode('utf-8').strip()
            assert content == expected_str, f"HTTP response is incorrect. Expected '{expected_str}', got '{content}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx on 127.0.0.1:8080: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error when testing Nginx proxy: {e}")

def test_processes_running():
    try:
        subprocess.check_output(["pgrep", "-f", "monitor"])
    except subprocess.CalledProcessError:
        pytest.fail("The 'monitor' process is not running")

    try:
        subprocess.check_output(["pgrep", "-f", "nginx"])
    except subprocess.CalledProcessError:
        pytest.fail("The 'nginx' process is not running")