# test_final_state.py

import os
import time
import subprocess
import pytest

def get_expected_count():
    count = 0
    with open("/app/large_access.log", "r") as f:
        for line in f:
            if "CRITICAL_ERROR" in line:
                count += 1
    return count

def test_execution_time_and_output():
    # Remove existing files to ensure we test the current run
    summary_path = "/home/user/alerts/summary.log"
    if os.path.exists(summary_path):
        os.remove(summary_path)

    expected_count = get_expected_count()

    start_time = time.time()
    result = subprocess.run(["env", "-i", "bash", "/home/user/monitor.sh"], capture_output=True)
    end_time = time.time()

    execution_time = end_time - start_time

    # Check execution time
    assert execution_time <= 1.5, f"Execution time {execution_time:.2f}s exceeded threshold of 1.5s"

    # Check script execution success
    assert result.returncode == 0, f"monitor.sh failed with return code {result.returncode}\nStderr: {result.stderr.decode()}"

    # Check summary.log exists
    assert os.path.exists(summary_path), f"{summary_path} was not created"

    # Check summary.log content
    with open(summary_path, "r") as f:
        content = f.read().strip()

    expected_content = f"Found {expected_count} critical errors"
    assert expected_content in content, f"Expected '{expected_content}' in summary.log, found '{content}'"

def test_email_sent():
    email_log_path = "/home/user/emails.log"
    assert os.path.exists(email_log_path), f"{email_log_path} does not exist. Is the SMTP server running and saving to this file?"

    expected_count = get_expected_count()
    expected_email_content = f"Found {expected_count} errors"

    with open(email_log_path, "r") as f:
        content = f.read()

    assert expected_email_content in content, f"Expected '{expected_email_content}' in {email_log_path}, but it was not found."