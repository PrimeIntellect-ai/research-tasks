# test_final_state.py

import pytest
import requests
import time

def test_api_artifact_endpoint():
    """Test that the HTTP server is running and returns the correct JSON response."""
    url = "http://127.0.0.1:8080/api/artifact"

    # Retry logic to wait for the server to be up, just in case
    max_retries = 5
    delay = 1
    response = None

    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            break
        except requests.exceptions.RequestException:
            if i < max_retries - 1:
                time.sleep(delay)
            else:
                pytest.fail(f"Failed to connect to the server at {url} after {max_retries} attempts.")

    assert response is not None, "Response should not be None."
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "version" in data, "The JSON response must contain a 'version' key."
    assert "determinant" in data, "The JSON response must contain a 'determinant' key."

    assert data["version"] == "2.1.4", f"Expected version '2.1.4', got {data['version']}"
    assert data["determinant"] == 29, f"Expected determinant 29, got {data['determinant']}"