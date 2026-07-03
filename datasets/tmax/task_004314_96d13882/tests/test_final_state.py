# test_final_state.py
import requests
import pytest

def test_api_user_a():
    """Test the API response for user A."""
    url = "http://127.0.0.1:8194/api/user_latency?user_id=A"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}. Is the server running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got invalid JSON: {response.text}")

    expected_data = [
        {"timestamp": "2023-10-01 10:00:00", "max_latency": 120.0},
        {"timestamp": "2023-10-01 10:10:00", "max_latency": 120.0},
        {"timestamp": "2023-10-01 10:20:00", "max_latency": 120.0},
        {"timestamp": "2023-10-01 10:30:00", "max_latency": 150.0}
    ]

    assert data == expected_data, f"Data for user A did not match expected.\nExpected: {expected_data}\nGot: {data}"

def test_api_user_b():
    """Test the API response for user B."""
    url = "http://127.0.0.1:8194/api/user_latency?user_id=B"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}. Is the server running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got invalid JSON: {response.text}")

    expected_data = [
        {"timestamp": "2023-10-01 10:00:00", "max_latency": 200.0},
        {"timestamp": "2023-10-01 10:10:00", "max_latency": 210.0}
    ]

    assert data == expected_data, f"Data for user B did not match expected.\nExpected: {expected_data}\nGot: {data}"