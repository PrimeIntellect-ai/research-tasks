# test_final_state.py
import pytest
import requests
import time

def test_unauthorized_endpoint():
    url = "http://127.0.0.1:9090/unauthorized"

    # Try to connect with a few retries in case the server is slow to start
    max_retries = 5
    response = None
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            break
        except requests.exceptions.RequestException:
            if i < max_retries - 1:
                time.sleep(1)
            else:
                pytest.fail(f"Failed to connect to the server at {url}. Ensure the server is running on 0.0.0.0:9090.")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Response body: {response.text}")

    expected_data = ["EMP007", "EMP042"]

    assert isinstance(data, list), f"Expected a JSON array, got {type(data).__name__}"
    assert sorted(data) == expected_data, f"Expected {expected_data}, got {data}"