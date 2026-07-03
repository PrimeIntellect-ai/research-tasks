# test_final_state.py

import os
import time
import json
import subprocess
import requests
import pytest

URL = "http://127.0.0.1:8080/metrics"
AUTH_HEADER = {"Authorization": "Bearer DataFlow2024"}
ARCHIVE_PATH = "/home/user/rolling_archive.jsonl"

def test_api_unauthorized():
    """Test that the API returns 401 when no auth token is provided."""
    try:
        response = requests.get(URL, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {URL}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for unauthorized access, got {response.status_code}"

def test_api_authorized():
    """Test that the API returns 200 and valid JSON when the correct auth token is provided."""
    try:
        response = requests.get(URL, headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert isinstance(data, dict), "Expected JSON response to be a dictionary"

    # Check that values are numbers
    for key, value in data.items():
        assert isinstance(key, str), f"Expected key {key} to be a string"
        assert isinstance(value, (int, float)), f"Expected value for {key} to be a number, got {type(value)}"

def test_crontab_configured():
    """Test that the user's crontab is configured to write to the archive file."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Is it configured?")

    assert "rolling_archive.jsonl" in crontab_content, "Crontab does not contain a job writing to rolling_archive.jsonl"

def test_rolling_archive_populated():
    """Test that the cron job populates the rolling archive file."""
    # Wait up to 65 seconds for the file to be created and populated
    timeout = 65
    start_time = time.time()

    while time.time() - start_time < timeout:
        if os.path.exists(ARCHIVE_PATH) and os.path.getsize(ARCHIVE_PATH) > 0:
            break
        time.sleep(2)

    assert os.path.exists(ARCHIVE_PATH), f"Archive file {ARCHIVE_PATH} was not created within {timeout} seconds"
    assert os.path.getsize(ARCHIVE_PATH) > 0, f"Archive file {ARCHIVE_PATH} is empty"

    with open(ARCHIVE_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) > 0, "No lines found in the archive file"

    # Verify the last line is valid JSON
    last_line = lines[-1].strip()
    try:
        data = json.loads(last_line)
    except ValueError:
        pytest.fail(f"Last line in archive file is not valid JSON: {last_line}")

    assert isinstance(data, dict), "Expected JSON line to be a dictionary"