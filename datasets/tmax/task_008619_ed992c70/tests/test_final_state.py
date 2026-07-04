# test_final_state.py
import os
import stat
import pytest

def test_config_env_contents():
    config_path = "/home/user/config.env"
    assert os.path.isfile(config_path), f"File {config_path} does not exist"
    with open(config_path, "r") as f:
        content = f.read()
    assert "TOKEN=ZGVwbG95X3NlY3JldA==" in content, f"{config_path} does not contain the expected token"

def test_crash_lock_exists():
    lock_path = "/home/user/crash.lock"
    assert os.path.isfile(lock_path), f"File {lock_path} was not created"

def test_worker_permissions():
    worker_path = "/home/user/worker"
    assert os.path.isfile(worker_path), f"Executable {worker_path} does not exist"

    st = os.stat(worker_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Permissions for {worker_path} are {oct(perms)}, expected 0o700"

def test_supervisor_permissions():
    supervisor_path = "/home/user/supervisor.sh"
    assert os.path.isfile(supervisor_path), f"Script {supervisor_path} does not exist"

    st = os.stat(supervisor_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Permissions for {supervisor_path} are {oct(perms)}, expected 0o700"

def test_supervisor_log_contents():
    log_path = "/home/user/supervisor.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Worker exited with 1",
        "Worker exited with 0"
    ]

    assert lines == expected_lines, f"Contents of {log_path} do not match the expected supervisor execution sequence. Got: {lines}"