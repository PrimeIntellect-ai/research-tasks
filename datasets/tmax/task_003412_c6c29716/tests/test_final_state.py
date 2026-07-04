# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080/api/v1/video-auth"

def test_ts_0():
    try:
        response = requests.get(f"{BASE_URL}?ts=0", timeout=10)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    assert response.text.strip() == "MjU=", f"Expected MjU=, got {response.text.strip()}"

def test_ts_1():
    try:
        response = requests.get(f"{BASE_URL}?ts=1", timeout=10)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    assert response.text.strip() == "MzI=", f"Expected MzI=, got {response.text.strip()}"

def test_ts_injection():
    try:
        response = requests.get(f"{BASE_URL}?ts=1;ls", timeout=10)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}. Response: {response.text}"
    assert response.text.strip() == "Invalid Input", f"Expected 'Invalid Input', got {response.text.strip()}"

def test_ts_3_malicious_qr():
    try:
        response = requests.get(f"{BASE_URL}?ts=3", timeout=10)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}. Response: {response.text}"
    assert response.text.strip() == "Invalid Input", f"Expected 'Invalid Input', got {response.text.strip()}"

def test_ts_4():
    try:
        response = requests.get(f"{BASE_URL}?ts=4", timeout=10)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    assert response.text.strip() == "OTA=", f"Expected OTA=, got {response.text.strip()}"