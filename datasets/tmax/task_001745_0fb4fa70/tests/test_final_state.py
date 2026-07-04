# test_final_state.py

import pytest
import requests
import time

URL = "http://127.0.0.1:8080/api/v1/projects"
AUTH_HEADER = {"Authorization": "Bearer GraphMaster2024"}

def wait_for_server(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(url, timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    return False

def test_server_running_and_unauthorized_without_token():
    # Wait briefly for the server to be available
    wait_for_server(URL)

    try:
        response = requests.get(URL, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the Go server on 127.0.0.1:8080. Is it running?")

    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

def test_unauthorized_with_invalid_token():
    try:
        response = requests.get(URL, headers={"Authorization": "Bearer InvalidToken123"}, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the Go server on 127.0.0.1:8080. Is it running?")

    assert response.status_code == 401, f"Expected 401 Unauthorized with invalid token, got {response.status_code}"

def test_authorized_request_returns_correct_result():
    try:
        response = requests.get(URL, headers=AUTH_HEADER, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the Go server on 127.0.0.1:8080. Is it running?")

    assert response.status_code == 200, f"Expected 200 OK with valid token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "result_count" in data, f"Response JSON missing 'result_count' key. Got: {data}"
    assert data["result_count"] == 5, f"Expected result_count to be 5, got {data['result_count']}"