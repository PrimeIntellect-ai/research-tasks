# test_final_state.py

import os
import stat
import pytest

def test_critical_utc_log_exists():
    """Test that the critical_utc.log file exists."""
    log_file = "/home/user/critical_utc.log"
    assert os.path.isfile(log_file), f"File {log_file} does not exist. The script might not have created it."

def test_critical_utc_log_permissions():
    """Test that the critical_utc.log file has 600 permissions."""
    log_file = "/home/user/critical_utc.log"
    assert os.path.isfile(log_file), f"File {log_file} does not exist."
    st = os.stat(log_file)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o600, f"Permissions of {log_file} are {oct(permissions)}, expected 0o600."

def test_critical_utc_log_content():
    """Test that the critical_utc.log file has the correct content."""
    log_file = "/home/user/critical_utc.log"
    assert os.path.isfile(log_file), f"File {log_file} does not exist."

    expected_lines = [
        "2023-11-01 03:45:00 UTC | Payment gateway timeout",
        "2023-11-01 16:30:00 UTC | Disk space critically low on /dev/sda1"
    ]

    with open(log_file, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines, but found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} mismatch. Expected: '{expected}', Got: '{actual.strip()}'"

def test_migrate_logs_sh_exists_and_executable():
    """Test that the migrate_logs.sh script exists and is executable."""
    script_file = "/home/user/migrate_logs.sh"
    assert os.path.isfile(script_file), f"Script {script_file} does not exist."

    st = os.stat(script_file)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"Script {script_file} is not executable."