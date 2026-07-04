# test_final_state.py

import pytest
import requests

def test_process_endpoint_success():
    url = "http://0.0.0.0:8080/process"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer SecretSysAdminKey123"
    }
    payload = {"data": [10, 3, 7, 2, 8, 5]}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "result" in data, f"Expected 'result' key in response JSON, got: {data}"
    assert data["result"] == [4, 6, 10, 14, 16, 20], f"Expected result [4, 6, 10, 14, 16, 20], got {data['result']}"

def test_process_endpoint_unauthorized():
    url = "http://0.0.0.0:8080/process"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer WrongKey"
    }
    payload = {"data": [1, 2, 3]}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected status 401 for invalid auth, got {response.status_code}. Response: {response.text}"

def test_process_endpoint_missing_auth():
    url = "http://0.0.0.0:8080/process"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {"data": [1, 2, 3]}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected status 401 for missing auth, got {response.status_code}. Response: {response.text}"