# test_final_state.py

import os
import re
import requests
import time
from datetime import datetime, timezone, timedelta

def test_service_running_and_timezone_fix():
    url = "http://127.0.0.1:8080/schedule"

    # Try a normal time
    payload = "time=23:59&job=test"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the service on port 8080: {e}"

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    # Check if response contains a Unix timestamp
    text = response.text.strip()
    assert re.search(r'\b\d{10}\b', text), f"Response does not contain a valid 10-digit Unix timestamp: {text}"

def test_boundary_condition_fix():
    url = "http://127.0.0.1:8080/schedule"

    # "24:00" is exactly 24 hours from the start of the current day
    payload = "time=24:00&job=test"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the service on port 8080: {e}"

    assert response.status_code == 200, f"Expected 200 OK for boundary time (24:00), got {response.status_code}. The off-by-one error (-ge 86400 vs -gt 86400) might not be fixed. Response: {response.text}"

def test_process_sh_fixes_applied():
    path = "/app/bash-http-scheduler/process.sh"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check for UTC fix
    assert 'UTC"' in content or "UTC" in content, "The timezone parsing bug does not appear to be fixed (missing 'UTC' in date command)."

    # Check for boundary fix
    assert "-gt 86400" in content or "-ge 86401" in content or "-ge 86400" not in content, "The boundary condition assertion (-ge 86400) does not appear to be fixed."