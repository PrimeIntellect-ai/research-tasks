# test_final_state.py

import os
import subprocess
import re
import pytest

def test_fstab_entry():
    fstab_path = "/home/user/fstab_entry.txt"
    assert os.path.isfile(fstab_path), f"Expected {fstab_path} to exist."

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    expected = "UUID=1234-5678 /home/user/metrics_data xfs defaults,noatime 0 0"
    # Replace multiple spaces with single space for robust comparison
    normalized_content = re.sub(r'\s+', ' ', content)
    assert normalized_content == expected, f"fstab entry does not match expected format. Got: {content}"

def test_deploy_script_and_execution():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Expected {script_path} to exist."
    assert os.access(script_path, os.X_OK), f"Expected {script_path} to be executable."

    # Execute the deploy script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"deploy.sh failed with exit code {result.returncode}. stderr: {result.stderr}"

def test_mail_mbox_appended():
    mail_path = "/home/user/mail.mbox"
    assert os.path.isfile(mail_path), f"Expected {mail_path} to exist."

    with open(mail_path, "r") as f:
        content = f.read()

    expected_headers = "To: observability-alerts@local.dev\nSubject: Deployment successful"
    expected_body = "The metrics proxy has been deployed."

    assert expected_headers in content, "mail.mbox is missing the expected headers."
    assert expected_body in content, "mail.mbox is missing the expected body."

def test_metrics_log_output():
    log_path = "/home/user/metrics_data/metrics.log"
    assert os.path.isfile(log_path), f"Expected {log_path} to exist after running deploy.sh."

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) >= 3, "metrics.log should contain at least 3 lines of output."

    # Check if ERROR line is present
    error_line_present = any("ERROR Memory leak detected" in line for line in lines)
    assert error_line_present, "The ERROR line was dropped. The bug in proxy.c was not fixed correctly."

    # Check timezone in timestamps (CET or CEST)
    for line in lines[-3:]:
        # Example format: [2023-10-24 10:00:00 CEST] INFO CPU usage...
        match = re.match(r'^\[(.*?) (CET|CEST)\]', line)
        assert match, f"Timestamp in log line does not contain the Europe/Zurich timezone (CET/CEST). Line: {line.strip()}"