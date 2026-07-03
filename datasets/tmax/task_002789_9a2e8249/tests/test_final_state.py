# test_final_state.py

import os
import re
import pytest
import requests
from requests.auth import HTTPBasicAuth

PORT = 8081
USER = "netadmin"
PASS = "pWd99xyz"
LOG_FILE = "/home/user/app_logs/service.log"
LOGROTATE_CONF = "/home/user/logrotate.conf"
BASE_URL = f"http://127.0.0.1:{PORT}"

def test_service_ping_authorized():
    """Test that the service is reachable, authenticated, and returns 'pong'."""
    try:
        response = requests.get(f"{BASE_URL}/ping", auth=HTTPBasicAuth(USER, PASS), timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service on port {PORT}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    assert response.text.strip() == "pong", f"Expected response body 'pong', got '{response.text}'"

def test_service_ping_unauthorized():
    """Test that the service rejects requests without auth or with bad auth."""
    try:
        response_no_auth = requests.get(f"{BASE_URL}/ping", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service on port {PORT}: {e}")

    assert response_no_auth.status_code == 401, f"Expected status 401 for missing auth, got {response_no_auth.status_code}"

    try:
        response_bad_auth = requests.get(f"{BASE_URL}/ping", auth=HTTPBasicAuth(USER, "wrongpass"), timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service on port {PORT}: {e}")

    assert response_bad_auth.status_code == 401, f"Expected status 401 for bad auth, got {response_bad_auth.status_code}"

def test_log_file_created():
    """Test that the log file is created in the correct absolute path."""
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."

def test_logrotate_config():
    """Test that the logrotate configuration is correct."""
    assert os.path.isfile(LOGROTATE_CONF), f"logrotate configuration {LOGROTATE_CONF} does not exist."

    with open(LOGROTATE_CONF, "r") as f:
        content = f.read()

    assert LOG_FILE in content, f"Log file path {LOG_FILE} not found in {LOGROTATE_CONF}"

    # Check for required directives
    assert re.search(r'\bdaily\b', content), f"'daily' directive missing in {LOGROTATE_CONF}"
    assert re.search(r'\brotate\s+7\b', content), f"'rotate 7' directive missing in {LOGROTATE_CONF}"
    assert re.search(r'\bcompress\b', content), f"'compress' directive missing in {LOGROTATE_CONF}"