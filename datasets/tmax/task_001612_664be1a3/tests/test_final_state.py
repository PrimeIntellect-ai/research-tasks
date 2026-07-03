# test_final_state.py
import os
import time
import pytest
import requests

BASE_URL = "http://127.0.0.1:5050"
HEADERS = {"Authorization": "Bearer net-graph-secret"}

def test_server_ready_file():
    """Verify that the agent created the /tmp/server_ready file."""
    assert os.path.isfile("/tmp/server_ready"), "The file /tmp/server_ready was not found. Did you create it after starting the server?"

def test_api_neighborhood_n1():
    """Verify the neighborhood cost for N1."""
    url = f"{BASE_URL}/api/neighborhood/N1"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200 for N1, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("node_id") == "N1", f"Expected node_id 'N1', got {data.get('node_id')}"
    assert data.get("neighborhood_cost") == 46.0, f"Expected neighborhood_cost 46.0 for N1, got {data.get('neighborhood_cost')}"

def test_api_neighborhood_n4():
    """Verify the neighborhood cost for N4."""
    url = f"{BASE_URL}/api/neighborhood/N4"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200 for N4, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("node_id") == "N4", f"Expected node_id 'N4', got {data.get('node_id')}"
    assert data.get("neighborhood_cost") == 47.0, f"Expected neighborhood_cost 47.0 for N4, got {data.get('neighborhood_cost')}"

def test_api_unauthorized():
    """Verify that the API requires the correct Authorization header."""
    url = f"{BASE_URL}/api/neighborhood/N1"

    # Missing header
    try:
        response_missing = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")
    assert response_missing.status_code in [401, 403], f"Expected 401 or 403 when missing Auth header, got {response_missing.status_code}"

    # Wrong token
    wrong_headers = {"Authorization": "Bearer wrong-secret"}
    try:
        response_wrong = requests.get(url, headers=wrong_headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")
    assert response_wrong.status_code in [401, 403], f"Expected 401 or 403 with wrong Auth token, got {response_wrong.status_code}"

def test_api_not_found():
    """Verify that the API returns 404 for a non-existent node."""
    url = f"{BASE_URL}/api/neighborhood/N99"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 404, f"Expected status code 404 for non-existent node N99, got {response.status_code}"