# test_final_state.py
import os
import re
import pytest

def test_login_exp_exists_and_executable():
    path = "/home/user/dashboard/login.exp"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_start_feed_sh_exists_and_executable():
    path = "/home/user/dashboard/start_feed.sh"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_feed_pid_exists_and_process_running():
    pid_file = "/home/user/dashboard/feed.pid"
    assert os.path.exists(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid numeric PID (found: {pid_str})."

    pid = int(pid_str)
    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} (from {pid_file}) is not running.")

    # Check if the process is expect
    cmdline_file = f"/proc/{pid}/cmdline"
    if os.path.exists(cmdline_file):
        with open(cmdline_file, "r") as f:
            cmdline = f.read().replace('\x00', ' ')
        assert "expect" in cmdline or "login.exp" in cmdline, f"Process {pid} does not appear to be the expect script (cmdline: {cmdline})"

def test_feed_log_exists_and_contains_correct_output():
    log_file = "/home/user/dashboard/feed.log"
    assert os.path.exists(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        log_content = f.read()

    assert "Dashboard feed active" in log_content, "Log file does not contain the success message 'Dashboard feed active'."
    assert "Authentication failed" not in log_content, "Log file contains 'Authentication failed'."
    assert "Error:" not in log_content, "Log file contains 'Error:' messages indicating missing environment variables."