# test_final_state.py

import os
import pytest
import requests

def test_server_pid_exists():
    """Verify that the server PID file exists and contains a valid PID."""
    pid_file = "/home/user/server.pid"
    assert os.path.isfile(pid_file), f"Missing PID file: {pid_file}"
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), f"PID file does not contain a valid integer: {pid_str}"

def test_unauthenticated_request():
    """Verify that an unauthenticated request returns a 401 Unauthorized."""
    url = "http://127.0.0.1:8000/stats"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_authenticated_request_and_response():
    """Verify that an authenticated request returns 200 and the correct JSON payload."""
    url = "http://127.0.0.1:8000/stats"
    headers = {"Authorization": "Bearer diff_token_99"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "N" in data, "Missing 'N' in JSON response"
    assert "k" in data, "Missing 'k' in JSON response"
    assert "D_app" in data, "Missing 'D_app' in JSON response"

    assert data["N"] == 240, f"Expected N=240, got {data['N']}"
    assert abs(data["k"] - 2.4) < 1e-5, f"Expected k=2.4, got {data['k']}"

    d_app = data["D_app"]
    assert isinstance(d_app, (int, float)), f"D_app must be a number, got {type(d_app)}"
    assert 40.0 <= d_app <= 50.0, f"Expected D_app to be between 40.0 and 50.0, got {d_app}"