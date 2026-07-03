# test_final_state.py

import os
import stat
import requests
import pytest

PORT = 8222
TOKEN = "tr0ub4dour"
URL = f"http://127.0.0.1:{PORT}/alert"

def test_webhook_unauthorized():
    """Test that the webhook rejects requests with missing or incorrect tokens."""
    try:
        response = requests.get(URL, headers={"Authorization": "Bearer wrongtoken"}, timeout=2)
        assert response.status_code == 401, f"Expected 401 Unauthorized for bad token, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to webhook server at {URL}. Is it running?")

def test_webhook_authorized():
    """Test that the webhook accepts authorized requests and returns the correct body."""
    try:
        response = requests.get(URL, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=2)
        assert response.status_code == 200, f"Expected 200 OK for valid token, got {response.status_code}"
        assert response.text.strip() == "Alert Logged", f"Expected body 'Alert Logged', got '{response.text}'"
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to webhook server at {URL}. Is it running?")

def test_system_state_after_alert():
    """Test that the webhook created the directory, set permissions, and wrote the log."""
    log_dir = "/home/user/alert_logs"
    log_file = os.path.join(log_dir, "alerts.txt")

    assert os.path.exists(log_dir), f"Directory {log_dir} was not created."
    assert os.path.isdir(log_dir), f"{log_dir} is not a directory."

    # Check permissions (700)
    dir_stat = os.stat(log_dir)
    perms = stat.S_IMODE(dir_stat.st_mode)
    assert perms == 0o700, f"Expected permissions 700 for {log_dir}, got {oct(perms)}"

    assert os.path.exists(log_file), f"Log file {log_file} was not created."
    assert os.path.isfile(log_file), f"{log_file} is not a file."

    with open(log_file, "r") as f:
        content = f.read()

    assert "Alert received" in content, f"Expected 'Alert received' in log file, got '{content}'"