# test_final_state.py

import pytest
import requests

def test_audit_page_1():
    url = "http://127.0.0.1:8080/audit?page=1&limit=2"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = {
        "data": [
            {"id": "D-98", "timestamp": 1600005000},
            {"id": "D-97", "timestamp": 1600004000}
        ],
        "total_descendants": 3,
        "page": 1
    }

    assert data == expected_data, f"Unexpected response data for page 1. Expected {expected_data}, got {data}"

def test_audit_page_2():
    url = "http://127.0.0.1:8080/audit?page=2&limit=2"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = {
        "data": [
            {"id": "D-95", "timestamp": 1600002000}
        ],
        "total_descendants": 3,
        "page": 2
    }

    assert data == expected_data, f"Unexpected response data for page 2. Expected {expected_data}, got {data}"