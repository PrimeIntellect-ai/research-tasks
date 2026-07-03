# test_final_state.py

import os
import pytest

def test_c_program_exists():
    c_file = "/home/user/analyze.c"
    assert os.path.exists(c_file), f"Missing required file: {c_file}"
    assert os.path.isfile(c_file), f"Expected {c_file} to be a file"

def test_executable_exists():
    exe_file = "/home/user/analyze"
    assert os.path.exists(exe_file), f"Missing executable: {exe_file}. Did you compile the program?"
    assert os.access(exe_file, os.X_OK), f"Expected {exe_file} to be executable"

def test_alerts_log():
    log_file = "/home/user/alerts.log"
    assert os.path.exists(log_file), f"Missing required file: {log_file}"

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["../../etc/shadow", "/usr/bin/system_update"]

    # Check if all expected files are in the log
    for exp in expected:
        assert exp in lines, f"Expected '{exp}' to be in {log_file}, but it was missing"

    # Check for no extra files
    for line in lines:
        assert line in expected, f"Unexpected file '{line}' found in {log_file}"

def test_safe_elfs_log():
    log_file = "/home/user/safe_elfs.log"
    assert os.path.exists(log_file), f"Missing required file: {log_file}"

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["safe_bins/safe_bin.elf"]

    # Check if all expected files are in the log
    for exp in expected:
        assert exp in lines, f"Expected '{exp}' to be in {log_file}, but it was missing"

    # Check for no extra files
    for line in lines:
        assert line in expected, f"Unexpected file '{line}' found in {log_file}"