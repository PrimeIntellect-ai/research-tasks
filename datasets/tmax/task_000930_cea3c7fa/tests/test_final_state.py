# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "9fXb2_Qz1"

def test_missing_auth():
    """Test that requests without an Authorization header are rejected."""
    url = f"{BASE_URL}/config/network"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 Forbidden for missing auth, got {response.status_code}. Response: {response.text}"

def test_invalid_auth():
    """Test that requests with an invalid Authorization header are rejected."""
    url = f"{BASE_URL}/config/network"
    headers = {"Authorization": "wrong_salt"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 Forbidden for invalid auth, got {response.status_code}. Response: {response.text}"

def test_valid_auth_existing_module_network():
    """Test that a valid request for an existing module returns the correct JSON data."""
    url = f"{BASE_URL}/config/network"
    headers = {"Authorization": API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for valid auth, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = [
        {"time": 1696161000, "user": "alice", "changes": ["+ dns=8.8.8.8"]},
        {"time": 1696165000, "user": "charlie", "changes": ["+ ip_forwarding=1"]}
    ]

    assert data == expected_data, f"Expected JSON data {expected_data}, got {data}"

def test_valid_auth_existing_module_database():
    """Test that a valid request for another existing module returns the correct JSON data."""
    url = f"{BASE_URL}/config/database"
    headers = {"Authorization": API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for valid auth, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = [
        {"time": 1696162500, "user": "bob", "changes": ["- max_conn=100", "+ max_conn=500"]}
    ]

    assert data == expected_data, f"Expected JSON data {expected_data}, got {data}"

def test_valid_auth_non_existent_module():
    """Test that a valid request for a non-existent module returns an empty list."""
    url = f"{BASE_URL}/config/unknown_module"
    headers = {"Authorization": API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for valid auth but unknown module, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data == [], f"Expected empty list [] for unknown module, got {data}"