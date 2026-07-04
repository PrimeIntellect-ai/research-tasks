# test_final_state.py

import os
import stat
import pytest

def test_safe_writer_c_exists_and_valid():
    c_file = "/home/user/safe_writer.c"
    assert os.path.isfile(c_file), f"{c_file} is missing"

    with open(c_file, "r") as f:
        content = f.read()

    assert "fcntl" in content, f"{c_file} must use fcntl for locking"
    assert "F_SETLKW" in content, f"{c_file} must use F_SETLKW for exclusive blocking lock"

def test_safe_writer_executable_exists():
    exe_file = "/home/user/safe_writer"
    assert os.path.isfile(exe_file), f"{exe_file} is missing"

    st = os.stat(exe_file)
    assert bool(st.st_mode & stat.S_IXUSR), f"{exe_file} is not executable"

def test_extract_sh_exists_and_valid():
    sh_file = "/home/user/extract.sh"
    assert os.path.isfile(sh_file), f"{sh_file} is missing"

    st = os.stat(sh_file)
    assert bool(st.st_mode & stat.S_IXUSR), f"{sh_file} is not executable"

    with open(sh_file, "r") as f:
        content = f.read()

    assert "&" in content, f"{sh_file} must run processes in the background using '&'"
    assert "wait" in content, f"{sh_file} must wait for background processes using 'wait'"
    assert "safe_writer" in content, f"{sh_file} must pipe to safe_writer"

def test_disk_alerts_log():
    log_file = "/home/user/disk_alerts.log"
    assert os.path.isfile(log_file), f"{log_file} is missing"

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "[DISK_FULL] Device /dev/sda1 is out of space",
        "[DISK_FULL] Write failed on /var/log",
        "[DISK_FULL] Quota exceeded for user backup",
        "[DISK_FULL] Cannot create temporary file"
    ]

    assert len(lines) == 4, f"{log_file} should contain exactly 4 lines, found {len(lines)}"

    for expected in expected_lines:
        assert expected in lines, f"Missing expected line in {log_file}: '{expected}'"