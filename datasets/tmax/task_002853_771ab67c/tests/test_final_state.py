# test_final_state.py
import os
import pytest

RESTORE_DIR = "/home/user/restore_test"

def test_restore_status_txt():
    status_file = os.path.join(RESTORE_DIR, "restore_status.txt")
    assert os.path.isfile(status_file), f"Missing file: {status_file}. The verify_restore.py script may not have been run or failed to create it."

    with open(status_file, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"File {status_file} is empty."
    assert lines[-1].strip() == "RESTORE VALIDATED", f"Last line of {status_file} is not 'RESTORE VALIDATED'. Found: {lines[-1]}"

def test_mail_log():
    mail_log = os.path.join(RESTORE_DIR, "logs/mail.log")
    assert os.path.isfile(mail_log), f"Missing file: {mail_log}. The verify_restore.py script may not have sent the email."

    with open(mail_log, "r") as f:
        content = f.read()

    assert "backup-success@localhost" in content, "Mail log is missing an email destined to 'backup-success@localhost'."
    assert "Restore Test Passed" in content, "Mail log is missing an email with the subject 'Restore Test Passed'."

def test_proxy_fixed():
    proxy_path = os.path.join(RESTORE_DIR, "proxy.py")
    assert os.path.isfile(proxy_path), f"Missing file: {proxy_path}"

    with open(proxy_path, "r") as f:
        content = f.read()

    assert "X-Backup-Restore-Test" not in content, "proxy.py still contains the 'X-Backup-Restore-Test' header check."

def test_healthcheck_fixed():
    healthcheck_path = os.path.join(RESTORE_DIR, "healthcheck.py")
    assert os.path.isfile(healthcheck_path), f"Missing file: {healthcheck_path}"

    with open(healthcheck_path, "r") as f:
        content = f.read()

    assert "smtplib.SMTP('127.0.0.1', 25)" not in content and "smtplib.SMTP(\"127.0.0.1\", 25)" not in content, "healthcheck.py still attempts to connect to port 25."
    assert "8025" in content, "healthcheck.py does not appear to be updated to use port 8025."