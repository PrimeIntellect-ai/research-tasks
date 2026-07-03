# test_final_state.py

import pytest
import requests
import time

def test_service_running_and_auth():
    """Test that the service is running and enforces authentication."""
    url = "http://127.0.0.1:8050/api/best_fit"

    # Try without auth token
    try:
        response_no_auth = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response_no_auth.status_code in [401, 403], \
        f"Expected 401 or 403 when missing auth token, got {response_no_auth.status_code}"

def test_service_correct_response():
    """Test that the service returns the correct JSON response with auth token."""
    url = "http://127.0.0.1:8050/api/best_fit"
    headers = {"X-Auth-Token": "physics-2024"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "optimal_c" in data, "Missing 'optimal_c' in JSON response"
    assert "mse" in data, "Missing 'mse' in JSON response"
    assert "datapoints_compared" in data, "Missing 'datapoints_compared' in JSON response"

    optimal_c = data["optimal_c"]
    mse = data["mse"]
    datapoints_compared = data["datapoints_compared"]

    assert isinstance(optimal_c, (int, float)), "optimal_c must be a number"
    assert 0.28 <= optimal_c <= 0.32, f"optimal_c {optimal_c} is not within the expected range [0.28, 0.32]"

    assert isinstance(mse, (int, float)), "mse must be a number"
    assert mse < 0.05, f"mse {mse} is too high (expected < 0.05)"

    assert isinstance(datapoints_compared, int), "datapoints_compared must be an integer"
    assert 290 <= datapoints_compared <= 310, f"datapoints_compared {datapoints_compared} is not close to 300"