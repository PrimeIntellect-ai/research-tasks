# test_final_state.py

import os
import re

def test_bash_profile_configured():
    path = "/home/user/.bash_profile"
    assert os.path.isfile(path), f"File {path} does not exist. You must create or modify it."

    with open(path, "r") as f:
        content = f.read()

    # Check for PATH export
    assert re.search(r"export\s+PATH=.*/home/user/custom_bin", content), \
        f"{path} does not properly export PATH with /home/user/custom_bin"

    # Check for MONITOR_LOG_DIR export
    assert re.search(r"export\s+MONITOR_LOG_DIR=/home/user/logs", content), \
        f"{path} does not properly export MONITOR_LOG_DIR=/home/user/logs"

def test_logs_directory_exists():
    path = "/home/user/logs"
    assert os.path.isdir(path), f"Directory {path} does not exist. You must create it."

def test_monitor_script_modifications():
    path = "/home/user/monitor.sh"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check if it sources .bash_profile
    assert re.search(r"(source|\.)\s+/home/user/\.bash_profile", content), \
        f"{path} does not source /home/user/.bash_profile"

    # Check if it uses text processing to filter services.conf
    assert re.search(r"(awk|sed|grep)", content), \
        f"{path} does not appear to use awk, sed, or grep to filter the configuration file."

def test_uptime_report_content():
    path = "/home/user/uptime_report.log"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the script?"

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "AuthService | 500 | 200 | DOWN",
        "Database | 200 | 200 | UP",
        "Cache | 200 | 200 | UP",
        "UnknownService | 404 | 200 | DOWN"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, found {len(lines)}."

    for expected, actual in zip(expected_lines, lines):
        assert actual == expected, f"Mismatch in {path}. Expected: '{expected}', Got: '{actual}'"