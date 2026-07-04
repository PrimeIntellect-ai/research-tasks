# test_final_state.py

import os
import re
import pytest

def test_backup_archive_exists_and_compressed():
    backup_path = "/home/user/archived_logs/backup.tar.gz"
    assert os.path.exists(backup_path), f"Backup archive not found at {backup_path}"
    assert os.path.isfile(backup_path), f"Backup path {backup_path} is not a file"

    file_size = os.path.getsize(backup_path)
    threshold = 25000
    assert file_size <= threshold, (
        f"Backup archive size is {file_size} bytes, which exceeds the threshold of {threshold} bytes. "
        "Make sure you are using gzip.BestCompression."
    )

def test_health_log_updated():
    health_log_path = "/home/user/health.log"
    assert os.path.exists(health_log_path), f"Health log not found at {health_log_path}"

    with open(health_log_path, "r") as f:
        content = f.read()

    assert "HEALTH CHECK: OK" in content, "Health log does not contain 'HEALTH CHECK: OK'"

def test_active_logs_empty():
    active_logs_dir = "/home/user/active_logs"
    assert os.path.exists(active_logs_dir), f"Active logs directory {active_logs_dir} is missing"

    files = os.listdir(active_logs_dir)
    log_files = [f for f in files if f.endswith(".log")]
    assert len(log_files) == 0, f"Active logs directory is not empty, found: {log_files}"

def test_crontab_content():
    crontab_path = "/home/user/final_crontab.txt"
    assert os.path.exists(crontab_path), f"Crontab file not found at {crontab_path}"

    with open(crontab_path, "r") as f:
        content = f.read()

    expected_path = "PATH=/usr/local/go/bin:/usr/bin:/bin:/home/user/log_manager/bin"
    assert expected_path in content, f"Crontab does not contain the correct PATH variable. Expected: {expected_path}"

    expected_cron = "*/15 * * * *"
    assert expected_cron in content, f"Crontab does not contain the correct schedule. Expected: {expected_cron}"

    assert "ACTIVE_LOGS=/home/user/active_logs" in content, "Crontab missing ACTIVE_LOGS environment variable"
    assert "BACKUP_DIR=/home/user/archived_logs" in content, "Crontab missing BACKUP_DIR environment variable"
    assert "/home/user/log_manager/bin/log_manager" in content, "Crontab missing the correct binary path execution"

def test_go_binary_compiled():
    binary_path = "/home/user/log_manager/bin/log_manager"
    assert os.path.exists(binary_path), f"Compiled Go binary not found at {binary_path}"
    assert os.path.isfile(binary_path), f"{binary_path} is not a file"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"