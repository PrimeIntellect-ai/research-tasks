# test_final_state.py

import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"
AUTH_HEADER = {"Authorization": "Bearer db-admin-token"}

def test_authorized_request_correct_traversal():
    url = f"{BASE_URL}/trace?start_node=NODE_77"
    try:
        response = requests.get(url, headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "infected_nodes" in data, "Response JSON missing 'infected_nodes' key"

    expected_nodes = {"NODE_77", "NODE_80", "NODE_81", "NODE_90", "NODE_95"}
    actual_nodes = set(data["infected_nodes"])

    assert actual_nodes == expected_nodes, f"Expected nodes {expected_nodes}, got {actual_nodes}"
    assert len(data["infected_nodes"]) == len(actual_nodes), "Response contains duplicated nodes, deduplication failed"

def test_unauthorized_request_no_header():
    url = f"{BASE_URL}/trace?start_node=NODE_77"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 401, f"Expected status code 401 for missing auth header, got {response.status_code}"

def test_unauthorized_request_wrong_token():
    url = f"{BASE_URL}/trace?start_node=NODE_77"
    headers = {"Authorization": "Bearer wrong-token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 401, f"Expected status code 401 for wrong token, got {response.status_code}"

def test_sql_injection_prevention():
    url = f"{BASE_URL}/trace?start_node=NODE_77' OR '1'='1"
    try:
        response = requests.get(url, headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected status code 200 (graceful handling of special characters via parameterization), got {response.status_code}"

    data = response.json()
    actual_nodes = set(data.get("infected_nodes", []))
    assert "NODE_80" not in actual_nodes, "SQL injection vulnerability detected; query returned unrelated nodes."