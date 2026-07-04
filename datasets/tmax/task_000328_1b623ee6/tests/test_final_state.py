# test_final_state.py

import os
import time
import subprocess
import pytest

APP_DIR = "/home/user/app"
PID_FILE = os.path.join(APP_DIR, "monitor.pid")
MAIL_SPOOL = os.path.join(APP_DIR, "mail_spool")
TARGET_STATUS = os.path.join(APP_DIR, "target_status.txt")
ALERT_EML = os.path.join(MAIL_SPOOL, "alert.eml")

def test_monitor_running():
    """Verify that the PID file exists and the monitor process is running."""
    assert os.path.exists(PID_FILE), "PID file missing."
    with open(PID_FILE, "r") as f:
        pid = f.read().strip()
    assert pid.isdigit(), "PID file does not contain a valid PID."

    try:
        os.kill(int(pid), 0)
    except OSError:
        pytest.fail(f"Monitor process {pid} is not running.")

def test_mail_spool_acls():
    """Verify the default POSIX ACLs on the mail_spool directory."""
    assert os.path.isdir(MAIL_SPOOL), "mail_spool directory missing."

    result = subprocess.run(["getfacl", MAIL_SPOOL], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run getfacl."

    output = result.stdout
    assert "default:user::rw-" in output, "Incorrect default user ACL on mail_spool."
    assert "default:group::r--" in output, "Incorrect default group ACL on mail_spool."
    assert "default:other::---" in output, "Incorrect default other ACL on mail_spool."

def test_monitor_behavior():
    """Verify that the monitor correctly processes a CRITICAL state and generates an alert."""
    assert os.path.exists(TARGET_STATUS), "target_status.txt missing."

    # Remove alert.eml if it exists from previous runs to ensure a fresh test
    if os.path.exists(ALERT_EML):
        os.remove(ALERT_EML)

    # Trigger the alert
    with open(TARGET_STATUS, "w") as f:
        f.write("CRITICAL\n")

    # Wait for the monitor to pick it up (up to 3 seconds)
    time.sleep(3)

    # Check if the target_status.txt was reset
    with open(TARGET_STATUS, "r") as f:
        status = f.read().strip()
    assert status == "OK", f"target_status.txt was not reset to OK. Current: '{status}'"

    # Check the email alert content
    assert os.path.exists(ALERT_EML), "alert.eml was not generated."

    expected_email = (
        "To: admin@local\n"
        "From: monitor@local\n"
        "Subject: Service Critical\n"
        "\n"
        "The monitored service reported a CRITICAL state."
    )

    with open(ALERT_EML, "r") as f:
        actual_email = f.read()

    assert actual_email.strip() == expected_email.strip(), "Email content mismatch."