# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_crash_time_file():
    """Verify that the crash time was correctly identified and written."""
    path = "/app/crash_time.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you create it?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_time = "2023-11-10T08:14:03Z"
    assert content == expected_time, f"Incorrect crash time in {path}. Expected '{expected_time}', got '{content}'"

def test_requirements_install():
    """Verify that requirements.txt has been fixed and installs without conflicts."""
    req_path = "/app/requirements.txt"
    assert os.path.isfile(req_path), f"File {req_path} is missing."

    result = subprocess.run(
        ["pip", "install", "-r", req_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pip install failed due to conflicts or errors:\n{result.stderr}\n{result.stdout}"

def test_api_health_endpoint_success():
    """Verify the Node.js API is running on the correct port and accepts the correct API key."""
    url = "http://127.0.0.1:9092/health"
    headers = {"X-API-KEY": "KAPPA-881-ALPHA"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to {url}. Is the Node.js service running on port 9092?")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected 200 OK at {url} with correct API key, got {response.status_code}. Response: {response.text}"

def test_api_health_endpoint_unauthorized():
    """Verify the Node.js API rejects requests without the correct API key."""
    url = "http://127.0.0.1:9092/health"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to {url}. Is the Node.js service running on port 9092?")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code in (401, 403), f"Expected 401 or 403 at {url} without API key, got {response.status_code}. The API must enforce the X-API-KEY header."