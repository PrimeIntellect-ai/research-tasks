# test_final_state.py

import os
import pytest

def test_deployment_log_contains_success():
    log_path = "/home/user/deployment.log"
    assert os.path.isfile(log_path), f"Deployment log {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "Deployment successful" in content, "The deployment.log does not contain 'Deployment successful'."

def test_production_binary_exists_and_executable():
    binary_path = "/home/user/deploy/production/monitor"
    assert os.path.isfile(binary_path), f"Production binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Production binary {binary_path} is not executable."

def test_mail_spool_contains_alert_email():
    spool_dir = "/home/user/mail_spool"
    assert os.path.isdir(spool_dir), f"Mail spool directory {spool_dir} does not exist."

    files = [os.path.join(spool_dir, f) for f in os.listdir(spool_dir) if os.path.isfile(os.path.join(spool_dir, f))]
    assert len(files) > 0, f"No files found in {spool_dir}. The monitor did not generate an email alert."

    found_valid_alert = False
    for file_path in files:
        with open(file_path, "r", errors="ignore") as f:
            content = f.read()

            has_subject = "Subject: ALERT: Service Down" in content
            has_from = "From: sre@localhost" in content or "From: <sre@localhost>" in content
            has_to = "To: admin@localhost" in content or "To: <admin@localhost>" in content

            if has_subject and has_from and has_to:
                found_valid_alert = True
                break

    assert found_valid_alert, "No email file in the mail spool contains the correct Subject, From, and To headers."