# test_final_state.py

import os
import stat
import pytest

def test_critical_archive_exists_and_contents():
    archive_path = "/home/user/critical_archive.log"
    assert os.path.isfile(archive_path), f"The archive file {archive_path} does not exist."

    expected_lines = {
        "[2023-01-01 10:05:00] [ERROR] [192.168.10.XXX] Database connection failed",
        "[2023-01-01 10:10:00] [CRITICAL] [172.16.0.XXX] Out of memory",
        "[2023-01-02 11:05:00] [ERROR] [8.8.8.XXX] DNS resolution failed"
    }

    with open(archive_path, "r") as f:
        actual_lines = {line.strip() for line in f if line.strip()}

    assert actual_lines == expected_lines, (
        f"Archive contents do not match expected.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )

def test_old_logs_deleted():
    old_files = [
        "/home/user/logs/old_app1.log",
        "/home/user/logs/old_app2.log"
    ]
    for file_path in old_files:
        assert not os.path.exists(file_path), f"Old log file {file_path} should have been deleted."

def test_new_logs_retained():
    new_files = [
        "/home/user/logs/new_app1.log",
        "/home/user/logs/new_app2.log"
    ]
    for file_path in new_files:
        assert os.path.isfile(file_path), f"New log file {file_path} should NOT have been deleted."

def test_binaries_and_scripts_executable():
    filter_bin = "/home/user/log_filter"
    script_sh = "/home/user/process_logs.sh"

    assert os.path.isfile(filter_bin), f"C++ binary {filter_bin} does not exist."
    assert os.access(filter_bin, os.X_OK), f"C++ binary {filter_bin} is not executable."

    assert os.path.isfile(script_sh), f"Shell script {script_sh} does not exist."
    assert os.access(script_sh, os.X_OK), f"Shell script {script_sh} is not executable."