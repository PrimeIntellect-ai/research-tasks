# test_final_state.py

import pytest
import requests

def test_server_response():
    url = "http://127.0.0.1:8080/stats"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Got: {response.text}")

    assert "empirical_mean" in data, f"Response JSON missing 'empirical_mean' key. Got: {data}"
    assert "sequence_count" in data, f"Response JSON missing 'sequence_count' key. Got: {data}"

    assert data["empirical_mean"] == 248, f"Expected empirical_mean to be 248, got {data['empirical_mean']}"
    assert data["sequence_count"] == 2, f"Expected sequence_count to be 2, got {data['sequence_count']}"