# test_final_state.py

import os
import pytest

def test_tcp_checker_cpp_exists():
    cpp_path = "/home/user/tcp_checker.cpp"
    assert os.path.isfile(cpp_path), f"{cpp_path} does not exist."
    with open(cpp_path, "r") as f:
        content = f.read()
    assert "main" in content, f"{cpp_path} does not seem to contain a valid C++ program."

def test_check_mount_conn_sh_exists():
    sh_path = "/home/user/check_mount_conn.sh"
    assert os.path.isfile(sh_path), f"{sh_path} does not exist."
    with open(sh_path, "r") as f:
        content = f.read()
    assert "tcp_checker" in content, f"{sh_path} does not seem to reference tcp_checker."

def test_mount_status_log_content():
    log_path = "/home/user/mount_status.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. The script may not have run successfully."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) > 0, f"{log_path} is empty."

    expected_log = "MOUNT_READY: storage_node at 127.0.0.1:8123"
    assert lines[-1] == expected_log, f"Expected the last log entry to be '{expected_log}', but got '{lines[-1]}'."

def test_executable_exists():
    exe_path = "/home/user/tcp_checker"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."