# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/evidence"
VALID_TOKEN = "8f9a2b4c6d8e0f1"
EXPECTED_DATA = {
    "files_accessed": ["/etc/shadow", "/root/.bash_history"],
    "malware_family": "Lazarus"
}

def test_api_valid_token():
    """Verify the API returns the correct data with a valid token."""
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
    try:
        response = requests.get(BASE_URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        json_data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, but failed to parse. Response: {response.text}")

    assert json_data == EXPECTED_DATA, f"Expected data {EXPECTED_DATA}, but got {json_data}"

def test_api_invalid_token():
    """Verify the API returns 401 Unauthorized with an invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    try:
        response = requests.get(BASE_URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {BASE_URL}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for invalid token, got {response.status_code}. Response: {response.text}"

def test_api_missing_token():
    """Verify the API returns 401 Unauthorized when the token is missing."""
    try:
        response = requests.get(BASE_URL, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {BASE_URL}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for missing token, got {response.status_code}. Response: {response.text}"