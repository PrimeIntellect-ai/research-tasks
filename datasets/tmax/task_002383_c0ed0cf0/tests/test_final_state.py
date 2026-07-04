# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer analyst_token_99"}

EXPECTED_VALUES = {
    1: 450,
    2: 100,
    3: 250,
    4: 25,
    5: 25,
    6: 150
}

def test_missing_auth():
    try:
        response = requests.get(f"{BASE_URL}/aggregate/1", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code in [401, 403], f"Expected 401 or 403 for missing auth, got {response.status_code}"

@pytest.mark.parametrize("node_id, expected_sum", EXPECTED_VALUES.items())
def test_aggregate_endpoint(node_id, expected_sum):
    try:
        response = requests.get(f"{BASE_URL}/aggregate/{node_id}", headers=AUTH_HEADER, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 200, f"Expected 200 OK for node {node_id}, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "node" in data, f"Missing 'node' in response JSON: {data}"
    assert "total_value" in data, f"Missing 'total_value' in response JSON: {data}"

    assert data["node"] == node_id, f"Expected node {node_id}, got {data['node']}"
    assert data["total_value"] == expected_sum, f"Expected total_value {expected_sum} for node {node_id}, got {data['total_value']}"

def test_invalid_auth():
    try:
        response = requests.get(f"{BASE_URL}/aggregate/1", headers={"Authorization": "Bearer invalid_token"}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code in [401, 403], f"Expected 401 or 403 for invalid auth, got {response.status_code}"