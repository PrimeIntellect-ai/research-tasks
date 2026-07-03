# test_final_state.py

import os
import re
import requests
import pytest
import time

def test_cron_file():
    """Test that the cron file is correctly formatted."""
    cron_path = "/home/user/pipeline.cron"
    assert os.path.isfile(cron_path), f"Cron file not found: {cron_path}"

    with open(cron_path, "r") as f:
        content = f.read().strip()

    assert "/home/user/pipeline.py" in content, "Cron file does not execute /home/user/pipeline.py"

    # Check for every 15 minutes schedule
    # Matches "*/15 * * * *" or "0,15,30,45 * * * *" etc.
    parts = content.split()
    assert len(parts) >= 6, "Cron file format seems invalid."
    minute_field = parts[0]
    assert minute_field in ("*/15", "0,15,30,45"), f"Cron schedule is not every 15 minutes. Found: {minute_field}"

def wait_for_server(url, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url)
            if r.status_code in (200, 400, 404):
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    return False

def test_api_u001():
    """Test the REST API for user U001, ensuring deduplication happened."""
    url = "http://127.0.0.1:8080/api/logs?user=U001"
    assert wait_for_server(url), "API server is not reachable at 127.0.0.1:8080"

    response = requests.get(url)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert "logs" in data, "Response JSON must contain a 'logs' key"

    logs = data["logs"]
    assert len(logs) == 1, f"Expected exactly 1 log for U001 after deduplication, got {len(logs)}"

    log = logs[0]
    assert log["timestamp"] == "2023-10-01T12:00:00Z", f"Incorrect timestamp: {log.get('timestamp')}"
    assert log["message"] == "First message", f"Incorrect message: {log.get('message')}"

def test_api_u002():
    """Test the REST API for user U002, ensuring multi-line messages are preserved."""
    url = "http://127.0.0.1:8080/api/logs?user=U002"
    assert wait_for_server(url), "API server is not reachable at 127.0.0.1:8080"

    response = requests.get(url)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert "logs" in data, "Response JSON must contain a 'logs' key"

    logs = data["logs"]
    assert len(logs) == 1, f"Expected exactly 1 log for U002, got {len(logs)}"

    log = logs[0]
    assert log["timestamp"] == "2023-10-01T13:00:00Z", f"Incorrect timestamp: {log.get('timestamp')}"
    assert log["message"] == "Line 1\nLine 2\nLine 3", f"Incorrect message, multi-line not preserved: {repr(log.get('message'))}"