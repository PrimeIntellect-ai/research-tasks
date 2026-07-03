# test_final_state.py

import os
import glob
import time
import socket
import subprocess
import pytest

def test_generate_report():
    """Verify that generate_report.sh extracts the correct home directory."""
    script_path = "/app/generate_report.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    try:
        output = subprocess.check_output([script_path, "charlie"], text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"{script_path} failed with exit code {e.returncode} and output: {e.output}")

    expected_output = "User charlie has home /home/charlie"
    assert expected_output in output.strip(), f"Expected '{expected_output}' in output, got: {output.strip()}"

def test_cron_backup():
    """Verify that cron_backup.sh writes backups to /app/backups/."""
    backup_dir = "/app/backups"

    # Wait for up to 10 seconds for the cron simulator to drop a backup
    found = False
    for _ in range(10):
        backups = glob.glob(os.path.join(backup_dir, "backup_*.tar.gz"))
        if backups:
            found = True
            break
        time.sleep(1)

    assert found, f"No backup_*.tar.gz files found in {backup_dir}. cron_backup.sh is likely still saving to the wrong directory."

def test_rotate_logs():
    """Verify that rotate_logs.sh correctly rotates and recreates the log file."""
    script_path = "/app/rotate_logs.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    test_log = "/app/test_rotation.log"
    test_log_rotated = test_log + ".1"

    # Create a test log with content
    with open(test_log, "w") as f:
        f.write("test log content")

    try:
        subprocess.check_call([script_path, test_log])
    except subprocess.CalledProcessError as e:
        pytest.fail(f"{script_path} failed during execution.")

    # Check rotated file
    assert os.path.isfile(test_log_rotated), f"Rotated log file {test_log_rotated} was not created."
    with open(test_log_rotated, "r") as f:
        content = f.read()
    assert content == "test log content", "Rotated log file does not contain the original content."

    # Check new file
    assert os.path.isfile(test_log), f"New log file {test_log} was not created."
    assert os.path.getsize(test_log) == 0, f"New log file {test_log} is not empty."

    # Check permissions (644)
    stat = os.stat(test_log)
    perms = oct(stat.st_mode)[-3:]
    assert perms == "644", f"New log file has incorrect permissions: {perms}, expected 644."

def test_account_daemon():
    """Verify that the account daemon listens on 8888, processes the command, and sends an email."""
    daemon_port = 8888
    spool_dir = "/app/mail_spool"

    # Record existing emails
    before_emails = set(glob.glob(os.path.join(spool_dir, "*.eml")))

    # Connect to the daemon and send the REPORT command
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(("127.0.0.1", daemon_port))
        s.sendall(b"REPORT charlie\n")
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to connect and send data to daemon on port {daemon_port}: {e}")

    # Wait for the email to be written by the mock SMTP server
    found = False
    for _ in range(15):
        after_emails = set(glob.glob(os.path.join(spool_dir, "*.eml")))
        new_emails = after_emails - before_emails

        for email_file in new_emails:
            with open(email_file, "rb") as f:
                content = f.read()
                if b"User charlie has home /home/charlie" in content:
                    found = True
                    break
        if found:
            break
        time.sleep(1)

    assert found, "The expected email containing the report output was not found in the mail spool."