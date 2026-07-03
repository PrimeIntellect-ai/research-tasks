# test_final_state.py

import os
import re
import pytest

def test_pid_file_exists_and_process_running():
    pid_file = "/home/user/run/daemon.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer PID. Found: '{pid_str}'"

    pid = int(pid_str)

    # Check if process is running
    cmdline_file = f"/proc/{pid}/cmdline"
    assert os.path.exists(cmdline_file), f"Process with PID {pid} is not running."

    with open(cmdline_file, "r") as f:
        cmdline = f.read().replace('\x00', ' ').strip()

    assert "daemon" in cmdline, f"Process {pid} is running, but it does not appear to be the daemon (cmdline: {cmdline})."

def test_daemon_output_log():
    log_file = "/home/user/logs/daemon_output.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing. The daemon did not write it."

    with open(log_file, "r") as f:
        content = f.read().strip()

    # The expected time is 2023-11-14 12:13:20
    # derived from TARGET_TIME=1700000000 and TZ=Pacific/Honolulu
    expected_time = "2023-11-14 12:13:20"

    assert expected_time in content, f"Log file {log_file} does not contain the correctly formatted time. Expected '{expected_time}', found '{content}'."