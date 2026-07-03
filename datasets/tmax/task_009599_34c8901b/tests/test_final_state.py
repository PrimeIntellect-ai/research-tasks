# test_final_state.py

import os
import re
import pytest
import subprocess

def test_c_code_modified():
    c_file_path = "/home/user/src/restore_monitor.c"
    assert os.path.isfile(c_file_path), f"C source file {c_file_path} is missing"

    with open(c_file_path, "r") as f:
        content = f.read()

    assert "getenv" in content, "getenv is not used in the modified C source file"
    assert "MONITOR_SOCK" in content, "The environment variable MONITOR_SOCK is not referenced in the C code"
    assert "/var/run/restore.sock" not in content, "The hardcoded socket path was not removed from the C code"

def test_executable_compiled():
    bin_path = "/home/user/bin/restore_monitor"
    assert os.path.isfile(bin_path), f"Executable {bin_path} is missing"
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable"

def test_bash_profile_updated():
    profile_path = "/home/user/.bash_profile"
    assert os.path.isfile(profile_path), f"Profile file {profile_path} is missing"

    with open(profile_path, "r") as f:
        content = f.read()

    # Look for export MONITOR_SOCK=/home/user/run/monitor.sock
    match = re.search(r"export\s+MONITOR_SOCK\s*=\s*['\"]?/home/user/run/monitor\.sock['\"]?", content)
    assert match is not None, "MONITOR_SOCK export is missing or incorrect in .bash_profile"

def test_cron_backup_file():
    cron_backup_path = "/home/user/cron_backup.txt"
    assert os.path.isfile(cron_backup_path), f"Cron backup file {cron_backup_path} is missing"

    with open(cron_backup_path, "r") as f:
        content = f.read()

    assert "*/5 * * * * /home/user/bin/restore_monitor" in content, "Cron backup file does not contain the correct cron job"

def test_actual_crontab():
    try:
        output = subprocess.check_output(['crontab', '-l'], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        output = ""

    assert "*/5 * * * * /home/user/bin/restore_monitor" in output, "The cron job is not actually scheduled in crontab"