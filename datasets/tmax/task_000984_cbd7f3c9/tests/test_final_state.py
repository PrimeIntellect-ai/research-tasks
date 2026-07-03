# test_final_state.py

import requests
import pytest

def test_server_running_and_responds_correctly():
    url = "http://127.0.0.1:8443/"
    headers = {
        "Authorization": "Bearer X79-PRECISION-BUILD"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the server on port 8443. Is the server running?")
    except requests.exceptions.Timeout:
        pytest.fail("Request to server on port 8443 timed out.")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred when connecting to the server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"
    assert "3.141592" in response.text, f"Expected '3.141592' in response body, but got: {response.text}"

def test_server_unauthorized():
    url = "http://127.0.0.1:8443/"
    headers = {
        "Authorization": "Bearer INVALID-TOKEN"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except Exception as e:
        pytest.fail(f"Failed to connect to the server for unauthorized test: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for invalid token, got {response.status_code}. Response: {response.text}"