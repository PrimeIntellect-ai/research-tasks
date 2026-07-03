# test_final_state.py

import os
import stat
import requests
import pytest

def test_api_status_success():
    """Verify that the API is accessible via Nginx, authorized, and returns the correct payload."""
    url = "http://127.0.0.1:8080/api/status"
    headers = {"Authorization": "Bearer X89F-SYS-BETA"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert data.get("status") == "operational", f"Expected JSON payload {{'status': 'operational'}}, got {data}"

def test_api_status_forbidden():
    """Verify that the API correctly rejects unauthorized requests."""
    url = "http://127.0.0.1:8080/api/status"
    headers = {"Authorization": "Bearer INVALID_TOKEN"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {url}: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 Forbidden for invalid token, got {response.status_code}. Response: {response.text}"

def test_socket_exists_and_is_socket():
    """Verify that the Unix domain socket was created at the correct path."""
    sock_path = "/home/user/backend/sockets/api.sock"
    assert os.path.exists(sock_path), f"Expected Unix socket at {sock_path} does not exist. Did the backend start and create it?"

    mode = os.stat(sock_path).st_mode
    assert stat.S_ISSOCK(mode), f"File at {sock_path} exists but is not a Unix domain socket."