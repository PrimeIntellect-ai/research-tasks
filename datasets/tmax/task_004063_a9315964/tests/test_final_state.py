# test_final_state.py

import hashlib
import pytest
import requests

# The expected secret key based on 13 red frames
SECRET_KEY = hashlib.sha256(b"RED_FRAMES_13").hexdigest()
BASE_URL = "http://127.0.0.1:8080"

def test_health_endpoint():
    """Verify the /health endpoint returns 200 OK with body 'OK'."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/health. Is the Go server running? Error: {e}")

    assert response.status_code == 200, f"Expected status code 200 for /health, got {response.status_code}"
    assert response.text == "OK", f"Expected body 'OK' for /health, got '{response.text}'"

def test_command_endpoint_unauthorized():
    """Verify the /command endpoint returns 401 Unauthorized when the secret key is missing."""
    try:
        response = requests.post(f"{BASE_URL}/command", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/command. Error: {e}")

    assert response.status_code == 401, f"Expected status code 401 for /command without X-Secret-Key header, got {response.status_code}"

def test_command_endpoint_authorized():
    """Verify the /command endpoint returns 200 OK with body 'COMMAND_ACCEPTED' when the correct secret key is provided."""
    headers = {"X-Secret-Key": SECRET_KEY}
    try:
        response = requests.post(f"{BASE_URL}/command", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/command. Error: {e}")

    assert response.status_code == 200, f"Expected status code 200 for /command with correct X-Secret-Key header, got {response.status_code}"
    assert response.text == "COMMAND_ACCEPTED", f"Expected body 'COMMAND_ACCEPTED' for /command, got '{response.text}'"