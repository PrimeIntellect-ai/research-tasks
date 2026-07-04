# test_final_state.py

import os
import glob
import re

def test_critical_summary_content():
    summary_path = "/home/user/migration/critical_summary.txt"
    assert os.path.isfile(summary_path), f"File {summary_path} does not exist."

    expected_lines = [
        "2023-10-12 14:21:12 | Database connection timeout",
        "2023-10-12 14:22:11 | Cache server unreachable",
        "2023-10-12 14:23:00 | Network partition detected",
        "2023-10-12 14:25:01 | File system read-only",
        "2023-10-12 14:26:00 | Process crashed unexpectedly",
        "2023-10-12 14:27:00 | Disk space 99% full"
    ]

    with open(summary_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {summary_path}, but found {len(content)}."

    for expected, actual in zip(expected_lines, content):
        assert expected == actual, f"Line mismatch in {summary_path}. Expected: '{expected}', Got: '{actual}'"

def test_backup_rotation():
    backup_dir = "/home/user/backups/"
    assert os.path.isdir(backup_dir), f"Backup directory {backup_dir} does not exist."

    tar_files = glob.glob(os.path.join(backup_dir, "*.tar.gz"))
    assert len(tar_files) == 3, f"Expected exactly 3 .tar.gz files in {backup_dir}, but found {len(tar_files)}: {tar_files}"

    oldest_backup = "/home/user/backups/backup_20231001_000000.tar.gz"
    assert not os.path.exists(oldest_backup), f"Oldest backup {oldest_backup} should have been deleted by rotation."

def test_email_alert_sent():
    # The mock SMTP server writes to sent_emails.log
    email_log_path = "/home/user/migration/sent_emails.log"
    migrator_script_path = "/home/user/migration/migrator.py"

    if os.path.isfile(email_log_path):
        with open(email_log_path, "r") as f:
            log_content = f.read()

        assert "Subject: Migration Alert: Critical Errors Detected" in log_content, "Email subject not found in sent emails."
        assert "migrator@cloudops.local" in log_content, "Sender email not found in sent emails."
        assert "admin@cloudops.local" in log_content, "Recipient email not found in sent emails."
        assert "Database connection timeout" in log_content, "Email body does not contain the critical summary contents."
    else:
        # Fallback to checking the script if the mock SMTP server didn't write the log
        assert os.path.isfile(migrator_script_path), f"{migrator_script_path} does not exist."
        with open(migrator_script_path, "r") as f:
            script_content = f.read()

        assert re.search(r"smtplib\.SMTP\s*\(\s*['\"]localhost['\"]\s*,\s*8025\s*\)", script_content) or \
               re.search(r"smtplib\.SMTP\s*\(\s*['\"]127\.0\.0\.1['\"]\s*,\s*8025\s*\)", script_content), \
               "Could not find smtplib.SMTP connection to localhost:8025 in migrator.py and sent_emails.log is missing."
        assert "Migration Alert: Critical Errors Detected" in script_content, "Expected email subject not found in migrator.py."
        assert "migrator@cloudops.local" in script_content, "Expected sender email not found in migrator.py."
        assert "admin@cloudops.local" in script_content, "Expected recipient email not found in migrator.py."