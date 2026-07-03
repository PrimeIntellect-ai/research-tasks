# test_final_state.py

import pytest
import requests

def test_server_response():
    url = "http://127.0.0.1:8080/status"
    headers = {"Authorization": "Bearer f8a92b1c4e7d3w5q"}

    try:
        response = requests.get(url, headers=headers, timeout=2.0)
    except requests.exceptions.Timeout:
        pytest.fail("Server request timed out. The timezone infinite loop bug might not be fixed, or the server is unresponsive.")
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the server. Ensure it is running and bound to 0.0.0.0:8080 or 127.0.0.1:8080.")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred while connecting to the server: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected a JSON response, but failed to parse it. Response text: {response.text}")

    assert data.get("status") == "ok", f"Expected 'status' to be 'ok', got: {data.get('status')}"
    assert data.get("timezone") == "Europe/Berlin", f"Expected 'timezone' to be 'Europe/Berlin', got: {data.get('timezone')}"