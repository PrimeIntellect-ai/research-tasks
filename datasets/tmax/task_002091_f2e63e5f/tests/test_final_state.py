# test_final_state.py

import pytest
import requests

def test_profile_endpoint():
    """
    Test that the HTTP server is running on 127.0.0.1:8000 and exposes the /profile endpoint
    with the correct JSON response.
    """
    url = "http://127.0.0.1:8000/profile"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Failed to connect to the server at {url}. The server is not running or listening on the wrong port.")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {url} timed out. The server is unresponsive.")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred while connecting to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response text: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")

    # Check thermal_limit
    assert "thermal_limit" in data, "The JSON response is missing the 'thermal_limit' key."
    assert data["thermal_limit"] == 82, f"Expected 'thermal_limit' to be 82, but got {data['thermal_limit']}."

    # Check dominant_freq_hz
    assert "dominant_freq_hz" in data, "The JSON response is missing the 'dominant_freq_hz' key."
    assert data["dominant_freq_hz"] == 140, f"Expected 'dominant_freq_hz' to be 140, but got {data['dominant_freq_hz']}."

    # Check optimal_rpm
    assert "optimal_rpm" in data, "The JSON response is missing the 'optimal_rpm' key."
    assert data["optimal_rpm"] == 2500, f"Expected 'optimal_rpm' to be 2500, but got {data['optimal_rpm']}."