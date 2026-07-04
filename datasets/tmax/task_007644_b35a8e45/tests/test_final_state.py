# test_final_state.py

import os
import pytest

def test_symlink_created():
    link_path = "/home/user/mnt_target"
    assert os.path.islink(link_path), f"Symlink {link_path} is missing or not a symlink."
    target = os.readlink(link_path)
    assert target == "/home/user/app_data", f"Symlink points to '{target}' instead of '/home/user/app_data'."

def test_app_log_content():
    log_path = "/home/user/app_data/app.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read()
    expected_text = "1.2.0 RUNNING MODE=PRODUCTION"
    assert expected_text in content, f"Expected '{expected_text}' in app.log, but got: '{content}'."

def test_rollout_script():
    script_path = "/home/user/rollout.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_worker_cpp_exists():
    cpp_path = "/home/user/src/worker.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."

def test_worker_pid_and_process():
    pid_file = "/home/user/run/worker.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: '{pid_str}'."
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process {pid} read from {pid_file} is not running.")

    cmdline_path = f"/proc/{pid}/cmdline"
    if os.path.isfile(cmdline_path):
        with open(cmdline_path, "r") as f:
            cmdline = f.read().replace('\0', ' ')
        assert "worker" in cmdline, f"Process {pid} does not appear to be the worker process. Command line: '{cmdline}'."