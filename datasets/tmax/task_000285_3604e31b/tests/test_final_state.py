# test_final_state.py

import os
import pytest

def test_directories_created():
    """Verify that the required directories have been created."""
    directories = [
        "/home/user/config",
        "/home/user/actual_configs",
        "/home/user/run",
        "/home/user/logs"
    ]
    for d in directories:
        assert os.path.isdir(d), f"Directory {d} is missing or not a directory."

def test_config_file_and_content():
    """Verify the config file exists and contains the exact expected lines."""
    config_path = "/home/user/actual_configs/current.conf"
    assert os.path.isfile(config_path), f"Config file {config_path} is missing."

    with open(config_path, "r") as f:
        content = f.read().strip()

    expected_content = "HEARTBEAT_FILE=/home/user/run/hb.txt\nTIMEOUT=2"
    assert content == expected_content, f"Config file content is incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_symlink_created_correctly():
    """Verify the symlink exists and points to the correct configuration file."""
    symlink_path = "/home/user/config/service.conf"
    target_path = "/home/user/actual_configs/current.conf"

    assert os.path.islink(symlink_path), f"Symlink {symlink_path} is missing or not a symlink."

    actual_target = os.readlink(symlink_path)
    assert actual_target == target_path, f"Symlink points to {actual_target} instead of {target_path}."

def test_supervisor_files_exist():
    """Verify the supervisor source and executable exist."""
    assert os.path.isfile("/home/user/supervisor.cpp"), "C++ source file /home/user/supervisor.cpp is missing."
    assert os.path.isfile("/home/user/supervisor"), "Executable /home/user/supervisor is missing."
    assert os.access("/home/user/supervisor", os.X_OK), "Executable /home/user/supervisor is not executable."

def test_alerts_log_content():
    """Verify the alerts.log file exists and contains exactly the expected output."""
    log_path = "/home/user/logs/alerts.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing. The supervisor may not have run correctly."

    with open(log_path, "r") as f:
        lines = f.readlines()

    expected_line = "ALERT: Process stalled. Restarting.\n"
    assert len(lines) == 2, f"Expected exactly 2 lines in {log_path}, found {len(lines)}."
    assert lines[0] == expected_line, f"First line of log is incorrect. Got: {lines[0]}"
    assert lines[1] == expected_line, f"Second line of log is incorrect. Got: {lines[1]}"