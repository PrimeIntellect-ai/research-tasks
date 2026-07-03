# test_final_state.py

import os
import subprocess
import time
import requests
import pytest

PORT = 9443
TOKEN = "SecureLogX99"
BASE_URL = f"http://127.0.0.1:{PORT}/"
SERVICE_DATA_DIR = "/home/user/service_data"
PROVISION_SCRIPT = "/home/user/provision.sh"
PID_FILE = os.path.join(SERVICE_DATA_DIR, "server.pid")
LOGROTATE_CONF = os.path.join(SERVICE_DATA_DIR, "logrotate.conf")
ACCESS_LOG = os.path.join(SERVICE_DATA_DIR, "access.log")

def test_provision_script_exists_and_executable():
    assert os.path.isfile(PROVISION_SCRIPT), f"{PROVISION_SCRIPT} does not exist."
    assert os.access(PROVISION_SCRIPT, os.X_OK), f"{PROVISION_SCRIPT} is not executable."

def test_http_server_unauthorized():
    try:
        response = requests.get(BASE_URL, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server on {BASE_URL}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for unauthorized request, got {response.status_code}"

def test_http_server_authorized():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.get(BASE_URL, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server on {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for authorized request, got {response.status_code}"
    assert response.text.strip() == "Authorized", f"Expected body 'Authorized', got '{response.text}'"

def test_logrotate_conf():
    assert os.path.isfile(LOGROTATE_CONF), f"{LOGROTATE_CONF} does not exist."
    with open(LOGROTATE_CONF, "r") as f:
        content = f.read()

    assert "daily" in content, "logrotate.conf missing 'daily' directive."
    assert "rotate 3" in content, "logrotate.conf missing 'rotate 3' directive."
    assert "compress" in content, "logrotate.conf missing 'compress' directive."
    assert "create 0644" in content or "create 644" in content, "logrotate.conf missing 'create 0644' directive."
    assert ACCESS_LOG in content, f"logrotate.conf does not target {ACCESS_LOG}."

def test_access_log_exists():
    assert os.path.isfile(ACCESS_LOG), f"{ACCESS_LOG} does not exist."

def test_idempotency():
    assert os.path.isfile(PID_FILE), f"{PID_FILE} does not exist."
    with open(PID_FILE, "r") as f:
        initial_pid = f.read().strip()

    assert initial_pid.isdigit(), f"PID file does not contain a valid PID: {initial_pid}"

    # Run provision.sh again
    result = subprocess.run([PROVISION_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"provision.sh failed on second run. stderr: {result.stderr}"

    with open(PID_FILE, "r") as f:
        second_pid = f.read().strip()

    assert initial_pid == second_pid, "PID changed after running provision.sh a second time. The script is not idempotent."

def test_server_still_running_after_idempotency_check():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.get(BASE_URL, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Server is no longer reachable after running provision.sh a second time: {e}")

    assert response.status_code == 200, "Server did not return 200 OK after idempotency check."