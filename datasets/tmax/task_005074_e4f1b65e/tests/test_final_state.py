# test_final_state.py

import os
import stat
import time
import requests
import pytest
from datetime import datetime

def test_logs_directory_permissions():
    """Verify /home/user/logs/ exists and has strictly 750 permissions."""
    log_dir = "/home/user/logs"
    assert os.path.isdir(log_dir), f"Directory {log_dir} does not exist."
    st = os.stat(log_dir)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o750, f"Expected {log_dir} permissions to be 750, but got {oct(perms)}."

def test_deploy_log_permissions():
    """Verify /home/user/logs/deploy.log exists and has strictly 640 permissions."""
    log_file = "/home/user/logs/deploy.log"
    assert os.path.isfile(log_file), f"File {log_file} does not exist."
    st = os.stat(log_file)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o640, f"Expected {log_file} permissions to be 640, but got {oct(perms)}."

def test_provision_script_executable():
    """Verify /home/user/provision.sh exists and is executable."""
    script_path = "/home/user/provision.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_webhook_server_installed():
    """Verify the webhook-server binary is installed in /home/user/.local/bin/."""
    bin_path = "/home/user/.local/bin/webhook-server"
    assert os.path.isfile(bin_path), f"Binary {bin_path} does not exist. Was it installed to the correct directory?"
    assert os.access(bin_path, os.X_OK), f"Binary {bin_path} is not executable."

def test_webhook_server_live_request():
    """
    Send a real HTTP POST request to the webhook server and verify the response
    as well as the side-effect in the deploy log.
    """
    url = "http://127.0.0.1:8080/deploy"
    payload = {"project": "alpha-omega"}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the webhook server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, but got {response.status_code}."

    # Wait a brief moment for the background script to write to the log
    time.sleep(0.5)

    log_file = "/home/user/logs/deploy.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing after triggering the webhook."

    with open(log_file, "r") as f:
        log_contents = f.read()

    expected_string = "Provisioning project: alpha-omega"
    assert expected_string in log_contents, (
        f"Expected string '{expected_string}' not found in {log_file}. "
        f"Actual contents:\n{log_contents}"
    )

    # Also verify the date format requirement
    today_iso = datetime.now().strftime("%Y-%m-%d")
    expected_line_prefix = f"[{today_iso}]"
    assert expected_line_prefix in log_contents, (
        f"Expected date prefix '{expected_line_prefix}' not found in {log_file}. "
        f"Actual contents:\n{log_contents}"
    )