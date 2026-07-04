# test_final_state.py
import os
import subprocess
import pytest

def test_pipeline_exists_and_executable():
    pipeline_path = '/home/user/pipeline.sh'
    assert os.path.isfile(pipeline_path), f"{pipeline_path} does not exist."
    assert os.access(pipeline_path, os.X_OK), f"{pipeline_path} is not executable."

def test_pipeline_execution_and_results():
    pipeline_path = '/home/user/pipeline.sh'

    # Run the pipeline
    result = subprocess.run([pipeline_path], capture_output=True, text=True)
    assert result.returncode == 0, f"pipeline.sh failed with return code {result.returncode}\nStderr: {result.stderr}"

    # Check Maildir structure
    for d in ['new', 'cur', 'tmp']:
        dir_path = f'/home/user/alerts_mail/{d}'
        assert os.path.isdir(dir_path), f"Maildir directory {dir_path} was not created."

    # Check idempotency
    make_result = subprocess.run(['make', '-C', '/home/user/src'], capture_output=True, text=True)
    assert make_result.returncode == 0, "Make failed on second run."
    output_lower = make_result.stdout.lower()
    assert "up to date" in output_lower or "nothing to be done" in output_lower, \
        f"Makefile is not idempotent. Output: {make_result.stdout}"

    # Check email content
    msg_path = '/home/user/alerts_mail/new/latest_alert.msg'
    assert os.path.isfile(msg_path), f"Alert message {msg_path} was not created."

    with open(msg_path, 'r') as f:
        content = f.read()

    assert "To: capacity-team@local.domain" in content, "Missing or incorrect 'To' header in email."
    assert "From: planner-bot@local.domain" in content, "Missing or incorrect 'From' header in email."
    assert "Subject: Capacity Alert" in content, "Missing or incorrect 'Subject' header in email."
    assert "ALERT_CPU_HIGH" in content, "Missing 'ALERT_CPU_HIGH' in email content."
    assert "ALERT_MEM_HIGH" in content, "Missing 'ALERT_MEM_HIGH' in email content."