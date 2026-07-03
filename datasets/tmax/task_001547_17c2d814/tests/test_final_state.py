# test_final_state.py

import requests
import pytest

def test_tensor_endpoint():
    url = "http://127.0.0.1:8080/tensor"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Is the Rust application running? Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Failed to parse response as JSON. Response body: {response.text}")

    expected_data = [[400, 800, 500], [1200, 300, 900]]
    assert data == expected_data, f"Expected JSON response {expected_data}, but got {data}"