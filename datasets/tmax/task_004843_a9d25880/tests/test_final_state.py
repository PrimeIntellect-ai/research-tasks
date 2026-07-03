# test_final_state.py

import os
import requests
import pytest

def test_libencoder_compiled():
    """Verify that the shared library was compiled."""
    so_path = "/app/libencoder.so"
    assert os.path.exists(so_path), f"Shared library missing: {so_path}"
    assert os.path.isfile(so_path), f"Expected {so_path} to be a file"

def test_mock_server_valid_request():
    """Verify the mock server responds correctly to a valid request."""
    url = "http://127.0.0.1:8080/api/v1/mock/encode"
    params = {"payload": "hello", "platform": "ios"}
    headers = {"Authorization": "Bearer mobile-ci-token-2024"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the mock server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert data.get("status") == "success", f"Expected status 'success', got: {data.get('status')}"

    expected_result = "ios_hello_X9F-44A-B21"
    assert data.get("result") == expected_result, f"Expected result '{expected_result}', got: {data.get('result')}"

def test_mock_server_unauthorized_request():
    """Verify the mock server returns 401 for unauthorized requests."""
    url = "http://127.0.0.1:8080/api/v1/mock/encode"
    params = {"payload": "test", "platform": "android"}

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the mock server: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}. Response: {response.text}"

def test_mock_server_different_payload():
    """Verify the mock server correctly encodes a different payload and platform."""
    url = "http://127.0.0.1:8080/api/v1/mock/encode"
    params = {"payload": "pytest_payload", "platform": "android"}
    headers = {"Authorization": "Bearer mobile-ci-token-2024"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the mock server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    expected_result = "android_pytest_payload_X9F-44A-B21"
    assert data.get("result") == expected_result, f"Expected result '{expected_result}', got: {data.get('result')}"