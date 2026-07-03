# test_final_state.py
import os
import stat
import pytest

def test_post_receive_hook_exists_and_executable():
    hook_path = "/home/user/monitor.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"The post-receive hook was not found at {hook_path}."
    assert os.access(hook_path, os.X_OK), f"The post-receive hook at {hook_path} is not executable."

def test_monitor_binary_exists_and_permissions():
    binary_path = "/home/user/bin/monitor"
    assert os.path.isfile(binary_path), f"The compiled binary was not found at {binary_path}."

    st = os.stat(binary_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o755, f"The binary at {binary_path} has permissions {oct(permissions)}, expected 0o755."

def test_alerts_log_content():
    pid_file = "/home/user/target.pid"
    assert os.path.isfile(pid_file), f"The PID file {pid_file} is missing."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"The PID file {pid_file} does not contain a valid integer."

    proc_comm_file = f"/proc/{pid_str}/comm"
    assert os.path.isfile(proc_comm_file), f"The target process (PID {pid_str}) is no longer running."

    with open(proc_comm_file, "r") as f:
        target_name = f.read().strip()

    expected_log = f"ALERT: Process {target_name} (PID {pid_str}) detected"

    log_file = "/home/user/alerts.log"
    assert os.path.isfile(log_file), f"The alerts log file {log_file} was not created."

    with open(log_file, "r") as f:
        log_content = f.read()

    assert expected_log in log_content, f"The expected log entry '{expected_log}' was not found in {log_file}."