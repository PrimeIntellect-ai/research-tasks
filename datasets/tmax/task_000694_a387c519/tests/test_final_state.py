# test_final_state.py

import pytest
import requests

def test_metrics_endpoint():
    url = "http://127.0.0.1:8080/metrics"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}. Is the service running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    expected_data = {
        "2023-10-01": 22,
        "2023-10-02": 20,
        "2023-10-03": 15
    }

    assert data == expected_data, f"JSON response data does not match expected output.\nExpected: {expected_data}\nGot: {data}"