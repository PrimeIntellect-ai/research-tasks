# test_final_state.py

import os
import gzip
import pytest

def test_executable_exists_and_executable():
    exe_path = "/home/user/bin/finops_backup"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_systemd_service_fixed():
    svc_path = "/home/user/.config/systemd/user/finops-backup.service"
    assert os.path.isfile(svc_path), f"Service file {svc_path} is missing."
    with open(svc_path, 'r') as f:
        content = f.read()

    # Check for After= and Requires= or Wants=
    assert "After=local-mailer.service" in content, "Service file is missing 'After=local-mailer.service'."
    assert ("Requires=local-mailer.service" in content or "Wants=local-mailer.service" in content), \
        "Service file should require or want local-mailer.service."

def test_backup_success_log():
    log_path = "/home/user/logs/backup_success.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created. Did the service run successfully?"
    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_text = "FinOps Backup Completed and Notification Sent"
    assert content == expected_text, f"Log file content is incorrect. Expected '{expected_text}', got '{content}'."

def test_archive_exists_and_valid():
    archive_path = "/home/user/archives/reports.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} was not created."

    # Check if it is a valid gzip file
    try:
        with gzip.open(archive_path, 'rb') as f:
            f.read(1) # Try to read a byte to ensure it's a valid gzip
    except Exception as e:
        pytest.fail(f"Archive {archive_path} is not a valid gzip file: {e}")