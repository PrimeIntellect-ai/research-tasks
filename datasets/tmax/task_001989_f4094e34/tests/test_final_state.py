# test_final_state.py

import pytest
import requests

URL = "http://127.0.0.1:9090/api/config"
CORRECT_TOKEN = "RECURSION_HALTED_4429"
EXPECTED_JSON = {
    "max_retries": "5",
    "timeout_seconds": "30",
    "log_level": "DEBUG",
    "enable_symlink_checks": "true",
    "backup_dir": "/var/backups/"
}

def test_server_running():
    """Verify that the server is listening and responding to requests."""
    try:
        requests.get(URL, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Could not connect to the server at {URL}. Is it running? Error: {e}")

def test_valid_request():
    """Verify that a request with the correct token returns 200 OK and the correct JSON."""
    headers = {"Authorization": f"Bearer {CORRECT_TOKEN}"}
    try:
        response = requests.get(URL, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, but could not parse body: {response.text}")

    assert data == EXPECTED_JSON, f"JSON response does not match expected output.\nExpected: {EXPECTED_JSON}\nGot: {data}"

def test_missing_auth():
    """Verify that a request missing the Authorization header returns 401 Unauthorized."""
    try:
        response = requests.get(URL, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for missing auth, got {response.status_code}. Response: {response.text}"

def test_wrong_auth():
    """Verify that a request with an incorrect token returns 401 Unauthorized."""
    headers = {"Authorization": "Bearer WRONG_TOKEN"}
    try:
        response = requests.get(URL, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for wrong auth, got {response.status_code}. Response: {response.text}"