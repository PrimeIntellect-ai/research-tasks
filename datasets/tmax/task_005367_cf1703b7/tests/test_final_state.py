# test_final_state.py

import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"
TOKEN = "AUTH-TOKEN-77X9-B2C4"

def test_health_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the health endpoint at {BASE_URL}/health: {e}")

    assert response.status_code == 200, f"Expected status code 200 for /health, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response for /health, got: {response.text}")

    assert data.get("status") == "ok", f"Expected {{'status': 'ok'}} for /health, got {data}"

def test_largest_endpoint_no_auth():
    try:
        response = requests.get(f"{BASE_URL}/largest", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the largest endpoint at {BASE_URL}/largest: {e}")

    assert response.status_code == 401, f"Expected status code 401 for /largest without auth, got {response.status_code}"

def test_largest_endpoint_wrong_auth():
    headers = {"Authorization": "Bearer WRONG-TOKEN"}
    try:
        response = requests.get(f"{BASE_URL}/largest", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the largest endpoint at {BASE_URL}/largest: {e}")

    assert response.status_code == 401, f"Expected status code 401 for /largest with wrong auth, got {response.status_code}"

def test_largest_endpoint_correct_auth():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.get(f"{BASE_URL}/largest", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the largest endpoint at {BASE_URL}/largest: {e}")

    assert response.status_code == 200, f"Expected status code 200 for /largest with correct auth, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response for /largest, got: {response.text}")

    assert isinstance(data, list), f"Expected JSON array for /largest, got {type(data)}"
    assert len(data) == 3, f"Expected exactly 3 items in the array, got {len(data)}"

    expected_data = [
        {"path": "logs_2023.zip/db.dump", "size": 750000},
        {"path": "logs_2023.zip/app.log", "size": 210000},
        {"path": "logs_2022.zip/auth.log", "size": 85000}
    ]

    assert data == expected_data, f"Expected top 3 largest files to be {expected_data}, but got {data}"