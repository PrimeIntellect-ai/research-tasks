# test_final_state.py
import requests
import pytest

def test_api_response():
    url = "http://127.0.0.1:8080/api/v1/corrupted_sizes"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    expected_data = [
        {
            "hostname": "prod-db-01",
            "total_corrupted_bytes": 8000
        },
        {
            "hostname": "prod-db-02",
            "total_corrupted_bytes": 7000
        }
    ]

    assert data == expected_data, f"Expected JSON response {expected_data}, but got {data}"