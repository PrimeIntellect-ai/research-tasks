# test_final_state.py

import pytest
import requests

def test_alert_endpoint():
    """Verify that the HTTP server is running and returns the correct JSON payload."""
    url = "http://127.0.0.1:8080/alert"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Failed to connect to the server at {url}. Is the server running?")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {url} timed out.")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred while requesting {url}: {e}")

    # Check status code
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response body: {response.text}"

    # Check Content-Type header
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type to include 'application/json', but got '{content_type}'"

    # Check JSON payload
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Failed to parse response body as JSON. Response body: {response.text}")

    expected_data = {
        "error_code": "E-72",
        "node_name": "omega 9",
        "node_ip": "10.0.0.42",
        "owner": "SRE-Team"
    }

    assert data == expected_data, f"JSON payload does not match expected output. Got: {data}, Expected: {expected_data}"