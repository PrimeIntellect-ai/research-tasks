# test_final_state.py

import pytest
import requests
import re
import datetime
import zoneinfo

def test_health_endpoint():
    """Test the GET /health endpoint for correct status and timezone."""
    try:
        response = requests.get("http://127.0.0.1:8080/health", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service on 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    body = response.text.strip()
    # Expecting format: YYYY-MM-DD HH:MM:SS %Z (where %Z is CET or CEST)
    match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (CET|CEST)", body)
    assert match is not None, f"Response body does not match expected date format and timezone (CET/CEST): {body}"

    # Check if the time is reasonably close to the current time in Europe/Berlin
    time_str = match.group(1)
    try:
        parsed_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        pytest.fail(f"Could not parse time string: {time_str}")

    tz = zoneinfo.ZoneInfo("Europe/Berlin")
    now = datetime.datetime.now(tz).replace(tzinfo=None)

    time_diff = abs((now - parsed_time).total_seconds())
    assert time_diff < 120, f"Returned time {parsed_time} is not within 120 seconds of current Europe/Berlin time {now}"

def test_alert_endpoint_success():
    """Test the POST /alert endpoint with the correct keyword."""
    try:
        response = requests.post("http://127.0.0.1:8080/alert", data="SHIBBOLETH", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service on 127.0.0.1:8080: {e}")

    assert response.status_code == 202, f"Expected status 202, got {response.status_code}"
    assert "TRIGGER_MAIL" in response.text, f"Expected 'TRIGGER_MAIL' in response body, got: {response.text}"

def test_alert_endpoint_failure():
    """Test the POST /alert endpoint with an incorrect keyword."""
    try:
        response = requests.post("http://127.0.0.1:8080/alert", data="WRONG", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service on 127.0.0.1:8080: {e}")

    assert response.status_code == 403, f"Expected status 403, got {response.status_code}"