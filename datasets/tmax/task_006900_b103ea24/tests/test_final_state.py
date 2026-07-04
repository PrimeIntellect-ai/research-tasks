# test_final_state.py

import os
import pytest

def test_backup_drive_created():
    dir_path = "/home/user/mnt/backup_drive"
    assert os.path.isdir(dir_path), f"Expected directory {dir_path} to exist."

def test_custom_fstab_created():
    fstab_path = "/home/user/custom_fstab"
    assert os.path.isfile(fstab_path), f"Expected file {fstab_path} to exist."

    with open(fstab_path, 'r') as f:
        content = f.read()

    expected_line = "monitor_fs /home/user/mnt/backup_drive customfs defaults 0 0"
    assert expected_line in content, f"Expected '{expected_line}' to be in {fstab_path}."

def test_monitor_c_modified():
    c_file_path = "/home/user/monitor.c"
    assert os.path.isfile(c_file_path), f"Expected C file {c_file_path} to exist."

    with open(c_file_path, 'r') as f:
        content = f.read()

    assert "/home/user/custom_fstab" in content, "Expected monitor.c to read from /home/user/custom_fstab."
    assert "/home/user/local_bin/perform_backup.sh" in content, "Expected monitor.c to use the absolute path to perform_backup.sh."

def test_monitor_daemon_compiled():
    daemon_path = "/home/user/monitor_daemon"
    assert os.path.isfile(daemon_path), f"Expected compiled binary {daemon_path} to exist."
    assert os.access(daemon_path, os.X_OK), f"Expected binary {daemon_path} to be executable."

def test_backup_executed():
    log_path = "/home/user/mnt/backup_drive/health_status.log"
    assert os.path.isfile(log_path), f"Expected log file {log_path} to exist. Did you run the compiled daemon?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content == "SYSTEM_HEALTHY", f"Expected log file content to be 'SYSTEM_HEALTHY', got '{content}'."