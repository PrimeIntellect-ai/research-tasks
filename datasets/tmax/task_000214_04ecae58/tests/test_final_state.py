# test_final_state.py
import requests
import pytest

URL = "http://127.0.0.1:9090/breaches"
VALID_TOKEN = "Bearer AUDIT_TOKEN_2024"

def test_server_running_and_unauthorized_without_header():
    try:
        response = requests.get(URL, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Server is not running on 127.0.0.1:9090 or endpoint /breaches is not exposed.")

    assert response.status_code == 401, f"Expected status code 401 without Authorization header, got {response.status_code}"

def test_server_unauthorized_with_invalid_header():
    headers = {"Authorization": "Bearer WRONG_TOKEN"}
    response = requests.get(URL, headers=headers, timeout=5)
    assert response.status_code == 401, f"Expected status code 401 with invalid Authorization header, got {response.status_code}"

def test_server_returns_correct_data():
    headers = {"Authorization": VALID_TOKEN}
    response = requests.get(URL, headers=headers, timeout=5)

    assert response.status_code == 200, f"Expected status code 200 with valid Authorization header, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON.")

    expected_data = [
        {
            "timestamp": 1730000008,
            "chain": ["Eve", "Frank", "Diana"]
        },
        {
            "timestamp": 1730000004,
            "chain": ["Alice", "Bob", "Diana"]
        }
    ]

    assert data == expected_data, f"Expected JSON response {expected_data}, but got {data}"