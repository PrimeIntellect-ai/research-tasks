# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"
ROOT_ID = "43981"
HEADERS = {"Authorization": f"Bearer {ROOT_ID}"}

def test_auth_missing_header():
    url = f"{BASE_URL}/manifest/1001"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 for missing auth header, got {response.status_code}. Response: {response.text}"

def test_auth_invalid_header():
    url = f"{BASE_URL}/manifest/1001"
    try:
        response = requests.get(url, headers={"Authorization": "Bearer 9999"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 for invalid auth header, got {response.status_code}. Response: {response.text}"

def test_manifest_parsing():
    url = f"{BASE_URL}/manifest/43981"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 for valid manifest request, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = {"name": "root-app", "version": "1.0"}
    assert data == expected_data, f"Expected JSON {expected_data}, got {data}"

def test_dependency_traversal():
    url = f"{BASE_URL}/dependencies/43981"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 for valid dependency request, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = [1001, 1002, 1003]
    assert data == expected_data, f"Expected JSON {expected_data}, got {data}"