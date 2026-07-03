# test_final_state.py

import os
import subprocess
import time
import pytest
import requests

def test_health_check_script():
    """Verify /app/health_check.sh exists, is executable, and works."""
    script_path = "/app/health_check.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

    # Run it and check output
    if os.path.exists("/tmp/health.log"):
        os.remove("/tmp/health.log")

    subprocess.run([script_path], check=True)

    assert os.path.exists("/tmp/health.log"), "/tmp/health.log was not created by the health check script"
    with open("/tmp/health.log", "r") as f:
        content = f.read().strip()
    assert "OK" in content, f"Expected 'OK' in /tmp/health.log, got '{content}'"

def test_cron_job_exists():
    """Verify the cron job is scheduled every 5 minutes."""
    try:
        # Try checking for user 'user'
        result = subprocess.run(["crontab", "-l", "-u", "user"], capture_output=True, text=True)
        cron_output = result.stdout
    except Exception:
        # Fallback to current user
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        cron_output = result.stdout

    assert "/app/health_check.sh" in cron_output, "Cron job for /app/health_check.sh not found"

    # Check for 5-minute schedule (e.g., "*/5 * * * *")
    valid_schedules = ["*/5", "0,5,10,15,20,25,30,35,40,45,50,55"]
    found_schedule = False
    for line in cron_output.splitlines():
        if "/app/health_check.sh" in line and not line.strip().startswith("#"):
            parts = line.strip().split()
            if parts[0] in valid_schedules:
                found_schedule = True
                break

    assert found_schedule, "Cron job is not scheduled to run every 5 minutes (expected */5 in minute field)"

def test_http_service_processing():
    """Verify the HTTP service processes encodings, cleans newlines, and gap-fills."""
    url = "http://127.0.0.1:9090/process"

    # We will send a UTF-16LE payload with embedded newlines and gaps
    # 1000,key1,"hello\nworld"
    # 1120,key1,"test"

    csv_data = '1000,key1,"hello\nworld"\n1120,key1,"test"\n'
    payload = csv_data.encode("utf-16le")

    try:
        response = requests.post(url, data=payload, headers={"Content-Type": "text/csv"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    result_text = response.text.strip()
    lines = result_text.splitlines()

    # Expected output after cleaning and gap-filling:
    # 1000,key1,"hello world"
    # 1060,key1,"hello world"
    # 1120,key1,"test"

    expected_lines = [
        '1000,key1,"hello world"',
        '1060,key1,"hello world"',
        '1120,key1,"test"'
    ]

    # Some implementations might strip quotes or leave them, but the values should match
    result_clean = [line.replace('"', '') for line in lines]
    expected_clean = [line.replace('"', '') for line in expected_lines]

    # Check if expected lines are in the result
    for expected in expected_clean:
        assert expected in result_clean, f"Expected line '{expected}' not found in output: {result_clean}"

def test_http_service_iso8859_1():
    """Verify the HTTP service handles ISO-8859-1 encoding."""
    url = "http://127.0.0.1:9090/process"

    csv_data = '2000,key2,"café"\n2060,key2,"done"\n'
    payload = csv_data.encode("iso-8859-1")

    try:
        response = requests.post(url, data=payload, headers={"Content-Type": "text/csv"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    result_text = response.text.strip()

    assert "café" in result_text or "caf\u00e9" in result_text, f"Failed to properly decode ISO-8859-1 payload. Output: {result_text}"