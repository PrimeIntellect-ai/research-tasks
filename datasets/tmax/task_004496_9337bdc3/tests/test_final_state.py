# test_final_state.py

import os
import smtplib
import subprocess
import tempfile
import time
import requests
import pytest
import re

def test_http_service():
    """Test the HTTP web service on port 8080."""
    url = "http://127.0.0.1:8080/transcript"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    expected_transcript = "Attention, the system update has been deployed successfully."
    actual_text = response.text.lower()

    # Strip punctuation for comparison
    expected_clean = re.sub(r'[^\w\s]', '', expected_transcript.lower())
    actual_clean = re.sub(r'[^\w\s]', '', actual_text)

    assert expected_clean in actual_clean, f"Expected transcript '{expected_transcript}' not found in response: {response.text}"

    # Check access log
    access_log = "/home/user/logs/access.log"
    assert os.path.isfile(access_log), f"Access log missing at {access_log}"
    with open(access_log, "r") as f:
        content = f.read()
        assert len(content.strip()) > 0, "Access log is empty after request"

def test_smtp_service():
    """Test the SMTP server on port 2525."""
    maillog_path = "/home/user/maillog.txt"
    if os.path.exists(maillog_path):
        initial_size = os.path.getsize(maillog_path)
    else:
        initial_size = 0

    test_subject = "Test Verifier Email"
    test_body = "This is a test payload from the verifier."
    message = f"Subject: {test_subject}\r\n\r\n{test_body}"

    try:
        with smtplib.SMTP("127.0.0.1", 2525, timeout=5) as server:
            server.ehlo("localhost")
            server.sendmail("test@verifier.local", ["admin@localhost"], message)
    except Exception as e:
        pytest.fail(f"Failed to communicate with SMTP server on 2525: {e}")

    time.sleep(1) # Give it a moment to write to the file

    assert os.path.isfile(maillog_path), f"Maillog missing at {maillog_path}"
    with open(maillog_path, "r") as f:
        content = f.read()
        assert test_subject in content, f"SMTP payload subject not found in {maillog_path}"
        assert test_body in content, f"SMTP payload body not found in {maillog_path}"

def test_git_hook():
    """Test the git post-receive hook."""
    deploy_git = "/home/user/deploy.git"
    app_code = "/home/user/app_code"
    deploy_log = "/home/user/logs/deploy.log"
    maillog = "/home/user/maillog.txt"

    assert os.path.isdir(deploy_git), f"Bare git repository missing at {deploy_git}"

    with tempfile.TemporaryDirectory() as temp_dir:
        # Clone the repo
        subprocess.run(["git", "clone", deploy_git, temp_dir], check=True, capture_output=True)

        # Create a dummy file and commit
        dummy_file = os.path.join(temp_dir, "dummy.txt")
        with open(dummy_file, "w") as f:
            f.write("test commit")

        subprocess.run(["git", "config", "user.email", "test@verifier.local"], cwd=temp_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Verifier"], cwd=temp_dir, check=True)
        subprocess.run(["git", "add", "dummy.txt"], cwd=temp_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Dummy commit"], cwd=temp_dir, check=True)

        # Push
        subprocess.run(["git", "push", "origin", "master"], cwd=temp_dir, check=True, capture_output=True)

    time.sleep(1) # Give hook time to execute

    # Check app_code
    assert os.path.isdir(app_code), f"App code directory missing at {app_code}"
    assert os.path.isfile(os.path.join(app_code, "dummy.txt")), "Pushed file not found in app_code directory"

    # Check deploy.log
    assert os.path.isfile(deploy_log), f"Deploy log missing at {deploy_log}"
    with open(deploy_log, "r") as f:
        content = f.read()
        assert len(content.strip()) > 0, "Deploy log is empty"

    # Check maillog for Subject: Code Pushed
    assert os.path.isfile(maillog), f"Maillog missing at {maillog}"
    with open(maillog, "r") as f:
        content = f.read()
        assert "Subject: Code Pushed" in content, "Expected 'Subject: Code Pushed' in maillog after git push"

def test_logrotate_config():
    """Test the logrotate configuration."""
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"Logrotate config missing at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "/home/user/logs/*.log" in content, "Target /home/user/logs/*.log not found in logrotate.conf"
    assert "daily" in content, "Keyword 'daily' not found in logrotate.conf"
    assert "rotate 5" in content, "Keyword 'rotate 5' not found in logrotate.conf"
    assert "compress" in content, "Keyword 'compress' not found in logrotate.conf"
    assert "missingok" in content, "Keyword 'missingok' not found in logrotate.conf"
    assert "su " not in content, "Found forbidden 'su' directive in logrotate.conf"