# test_final_state.py

import pytest
import requests

def test_api_centrality():
    url = "http://127.0.0.1:8000/centrality"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    expected_data = {"10": 2, "20": 1}

    assert data == expected_data, f"Expected JSON response {expected_data}, but got {data}"