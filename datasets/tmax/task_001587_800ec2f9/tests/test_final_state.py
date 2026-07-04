# test_final_state.py

import os
import pytest

def test_backup_directory_exists():
    backup_dir = "/home/user/backups"
    assert os.path.isdir(backup_dir), f"Backup directory '{backup_dir}' does not exist. Did you create it?"

def test_check_deploy_executable():
    executable_path = "/home/user/monitor/check_deploy"
    assert os.path.isfile(executable_path), f"Executable '{executable_path}' not found. Did you compile your C++ code?"
    assert os.access(executable_path, os.X_OK), f"File '{executable_path}' is not executable."

def test_alerts_log():
    log_path = "/home/user/monitor/alerts.log"
    assert os.path.isfile(log_path), f"Log file '{log_path}' does not exist. Did the program log alerts?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_v2 = "ALERT: Target v2 failed. Reason: SocketError"
    expected_v3 = "ALERT: Target v3 failed. Reason: ConfigError"

    assert expected_v2 in lines, f"Expected alert for v2 not found in {log_path}. Found: {lines}"
    assert expected_v3 in lines, f"Expected alert for v3 not found in {log_path}. Found: {lines}"

    # Verify no v1 alert
    for line in lines:
        assert "v1" not in line, f"Unexpected alert for v1 found in {log_path}: '{line}'"

def test_backups_created():
    backup_v2 = "/home/user/backups/failed_v2.tar.gz"
    backup_v3 = "/home/user/backups/failed_v3.tar.gz"

    assert os.path.isfile(backup_v2), f"Backup archive '{backup_v2}' does not exist. Did the program create a backup for v2?"
    assert os.path.isfile(backup_v3), f"Backup archive '{backup_v3}' does not exist. Did the program create a backup for v3?"

    # Ensure they are gzip files (check magic number)
    for backup_file in [backup_v2, backup_v3]:
        with open(backup_file, "rb") as f:
            magic = f.read(2)
            assert magic == b'\x1f\x8b', f"File '{backup_file}' does not appear to be a gzip-compressed archive."

def test_no_v1_backup():
    backup_v1 = "/home/user/backups/failed_v1.tar.gz"
    assert not os.path.exists(backup_v1), f"Backup archive '{backup_v1}' should NOT exist, as v1 is a valid deployment."