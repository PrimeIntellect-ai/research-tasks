# test_final_state.py

import os
import requests
import pytest

DASHBOARD_URL = "http://127.0.0.1:8080/api/status"
AUTH_TOKEN = "SRE-M0N-8821"

def test_api_status_unauthorized_no_token():
    """Test that the API returns 401 when no token is provided."""
    try:
        response = requests.get(DASHBOARD_URL, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the dashboard at {DASHBOARD_URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

def test_api_status_unauthorized_wrong_token():
    """Test that the API returns 401 when an incorrect token is provided."""
    headers = {"Authorization": "Bearer WRONG-TOKEN"}
    try:
        response = requests.get(DASHBOARD_URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the dashboard at {DASHBOARD_URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized with wrong token, got {response.status_code}"

def test_api_status_authorized():
    """Test that the API returns 200 OK with the correct token and valid JSON."""
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    try:
        response = requests.get(DASHBOARD_URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the dashboard at {DASHBOARD_URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK with correct token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, but failed to parse. Response text: {response.text}")

    assert isinstance(data, dict), "Expected JSON response to be a dictionary"

def test_variance_debug_file():
    """Test that the variance debug file is created and contains a valid float."""
    path = "/home/user/variance_debug.txt"
    assert os.path.isfile(path), f"Missing variance debug file at {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        variance = float(content)
    except ValueError:
        pytest.fail(f"Expected a valid float in {path}, but got: {content}")

    assert variance >= 0, f"Variance cannot be negative, got: {variance}"

def test_health_json_exists():
    """Test that the Go checker successfully wrote the health data."""
    path = "/tmp/health.json"
    assert os.path.isfile(path), f"Missing health data file at {path}. The Go checker might have failed or not run."