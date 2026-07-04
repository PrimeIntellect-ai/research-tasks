# test_final_state.py

import pytest
import requests
import time

def test_solution_endpoint():
    """Verify that the HTTP API server is running and returns the correct solution."""
    url = "http://127.0.0.1:8000/solution"

    # Try to connect a few times in case the server is slow to start
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            break
        except requests.exceptions.RequestException:
            if attempt == max_retries - 1:
                pytest.fail(f"Failed to connect to the server at {url}. Is it running?")
            time.sleep(1)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "S" in data, f"Response JSON missing key 'S'. Got: {data}"

    # The expected value is 4.502
    expected_s = 4.502
    actual_s = data["S"]

    assert isinstance(actual_s, (int, float)), f"Value of 'S' must be a number, got {type(actual_s)}"
    assert round(actual_s, 3) == expected_s, f"Expected S to be {expected_s}, but got {actual_s}"