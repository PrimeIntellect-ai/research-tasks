# test_final_state.py

import requests
import pytest

def test_auth_service_running_and_fixed():
    url = "http://127.0.0.1:8888/verify"
    headers = {
        "X-API-Key": "sec_k99x_memory_extracted_7721",
        "Content-Type": "application/json"
    }

    # Test with a username containing a space (the regression)
    payload_with_space = {
        "username": "Valid Space",
        "token": "abcdefghijklmnop"
    }

    try:
        response = requests.post(url, headers=headers, json=payload_with_space, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("The auth service is not running or not listening on 127.0.0.1:8888.")
    except requests.exceptions.Timeout:
        pytest.fail("The auth service timed out.")

    assert response.status_code == 200, f"Expected HTTP 200 OK for username with space, got {response.status_code}. Response: {response.text}"

def test_auth_service_normal_username():
    url = "http://127.0.0.1:8888/verify"
    headers = {
        "X-API-Key": "sec_k99x_memory_extracted_7721",
        "Content-Type": "application/json"
    }

    # Test with a normal username (should also work)
    payload_normal = {
        "username": "AdminUser",
        "token": "1234567890123456"
    }

    try:
        response = requests.post(url, headers=headers, json=payload_normal, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for normal username, got {response.status_code}. Response: {response.text}"

def test_auth_service_invalid_auth():
    url = "http://127.0.0.1:8888/verify"
    headers = {
        "X-API-Key": "wrong_key",
        "Content-Type": "application/json"
    }

    payload = {
        "username": "AdminUser",
        "token": "1234567890123456"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code in [401, 403], f"Expected HTTP 401 or 403 for invalid API key, got {response.status_code}."