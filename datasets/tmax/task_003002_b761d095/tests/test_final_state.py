# test_final_state.py
import pytest
import requests
import time

def test_pattern_endpoint():
    """
    Test that the HTTP server is running on 127.0.0.1:8080 and returns the correct JSON
    for the /pattern endpoint.
    """
    url = "http://127.0.0.1:8080/pattern"

    # Retry a few times in case the server is slow to start, though it should be running
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            break
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                pytest.fail(f"Failed to connect to the server at {url}: {e}")
            time.sleep(1)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = {"path": ["web01", "lb01", "db01"]}
    assert data == expected_data, f"Expected JSON {expected_data}, but got {data}"