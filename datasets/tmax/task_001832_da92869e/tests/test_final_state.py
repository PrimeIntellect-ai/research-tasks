# test_final_state.py

import pytest
import requests
import time

def test_api_unauthorized():
    """Test that the API returns 401 Unauthorized when the auth token is missing."""
    url = "http://localhost:8080/api/stats"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("API service is not running or not listening on port 8080.")
    except requests.exceptions.Timeout:
        pytest.fail("API request timed out.")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}. Response: {response.text}"

def test_api_stats_correct():
    """Test that the API returns the correct vehicle counts when authenticated."""
    url = "http://localhost:8080/api/stats?auth=vision2024"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("API service is not running or not listening on port 8080.")
    except requests.exceptions.Timeout:
        pytest.fail("API request timed out.")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"API did not return valid JSON. Response: {response.text}")

    expected_data = {
        "status": "success",
        "data": {
            "northbound": 42,
            "southbound": 17
        }
    }

    assert data == expected_data, f"API returned incorrect data. Expected {expected_data}, got {data}"