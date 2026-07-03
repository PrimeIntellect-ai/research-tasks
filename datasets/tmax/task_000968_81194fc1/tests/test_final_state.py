# test_final_state.py

import os
import tarfile
import pytest

def test_valid_emails_content():
    file_path = "/home/user/project/valid_emails.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    expected = ["admin@example.com", "user@domain.com"]
    assert content == expected, f"Content of {file_path} does not match expected valid emails. Got: {content}"

def test_backup_script_exists_and_executable():
    script_path = "/home/user/backup.sh"
    assert os.path.isfile(script_path), f"Backup script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Backup script {script_path} is not executable."

def test_backup_archive_exists_and_valid():
    archive_path = "/home/user/backups/project_backup.tar.gz"
    assert os.path.isfile(archive_path), f"Backup archive {archive_path} is missing."

    # Check if it's a valid tar.gz file
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            members = tar.getnames()
            assert len(members) > 0, "Tar archive is empty."
    except tarfile.ReadError:
        pytest.fail(f"File {archive_path} is not a valid gzip-compressed tar archive.")

def test_notification_email_content():
    file_path = "/home/user/mail_spool/notification.txt"
    assert os.path.isfile(file_path), f"Notification file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "BUILD SUCCESS", f"Notification file content is incorrect. Expected 'BUILD SUCCESS', got '{content}'"

def test_ci_daemon_fixed():
    script_path = "/home/user/ci_daemon.sh"
    assert os.path.isfile(script_path), f"Daemon script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Daemon script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    # Check for basic error handling like set -e
    assert "set -e" in content or "set -o errexit" in content, "Daemon script does not appear to have 'set -e' for error handling."
    # Ensure the syntax error is gone (the missing 'then')
    # It's hard to parse bash strictly in python, but we can check if 'then' exists now
    assert "then" in content, "Daemon script seems to still be missing 'then' in its if-statement."