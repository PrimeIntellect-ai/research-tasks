# test_final_state.py

import os
import re
import hashlib
import requests
import pytest

def test_cron_file_exists_and_correct():
    cron_file = "/home/user/log_rotate.cron"
    assert os.path.exists(cron_file), f"Cron file {cron_file} does not exist."

    with open(cron_file, 'r') as f:
        content = f.read().strip()

    # Valid cron syntax for midnight daily
    # 0 0 * * * /usr/bin/logrotate -f /etc/logrotate.d/tracker
    # Allow some whitespace variations
    pattern = r"^0\s+0\s+\*\s+\*\s+\*\s+/usr/bin/logrotate\s+-f\s+/etc/logrotate\.d/tracker$"
    assert re.match(pattern, content), f"Cron file content does not match expected pattern. Got: {content}"

def test_http_server_valid_request():
    url = "http://127.0.0.1:9090/track"
    payload = {
        "timestamp": "2023-10-25T14:30:00Z",
        "service": "api-gateway",
        "config_data": "max_connections=100\ntimeout=30"
    }

    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for valid payload, got {response.status_code}"

def test_http_server_invalid_service():
    url = "http://127.0.0.1:9090/track"
    payload = {
        "timestamp": "2023-10-25T14:30:00Z",
        "service": "my service", # invalid space
        "config_data": "test"
    }

    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 400, f"Expected HTTP 400 for invalid service, got {response.status_code}"

def test_http_server_invalid_timestamp():
    url = "http://127.0.0.1:9090/track"
    payload = {
        "timestamp": "25-10-2023", # invalid format
        "service": "api-gateway",
        "config_data": "test"
    }

    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 400, f"Expected HTTP 400 for invalid timestamp, got {response.status_code}"

def test_log_file_content():
    log_file = "/home/user/tracked_configs.log"
    assert os.path.exists(log_file), f"Log file {log_file} does not exist."

    with open(log_file, 'r') as f:
        content = f.read()

    expected_hash = hashlib.md5(b"max_connections=100\ntimeout=30").hexdigest().upper()
    expected_line = f"[2023-10-25T14:30:00Z] api-gateway | SIGNATURE: {expected_hash}"

    assert expected_line in content, f"Expected line '{expected_line}' not found in log file. Content: {content}"