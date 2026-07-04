# test_final_state.py
import os
import requests
import pytest
import time

def test_rust_binary_compiled():
    binary_path = "/home/user/math_engine/target/release/math_engine"
    assert os.path.isfile(binary_path), f"Rust binary not found at {binary_path}. Did you compile it in release mode?"
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable."

def test_go_server_unauthorized():
    url = "http://127.0.0.1:8080/compute"

    # Test missing auth header
    try:
        response = requests.post(url, json={"value": 5}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Go server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth header, got {response.status_code}"

    # Test invalid auth header
    headers = {"Authorization": "Bearer InvalidToken"}
    response = requests.post(url, json={"value": 5}, headers=headers, timeout=2)
    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid auth header, got {response.status_code}"

def test_go_server_authorized_compute():
    url = "http://127.0.0.1:8080/compute"
    headers = {"Authorization": "Bearer Sigma77Omega"}

    # Test N = 10
    payload = {"value": 10}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Go server at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "computed" in data, f"Response missing 'computed' key: {data}"

    # Allow small floating point differences, but expect exactly 27.182818 based on the constant 2.7182818
    expected = 27.182818
    assert abs(data["computed"] - expected) < 1e-6, f"Expected computed value close to {expected}, got {data['computed']}"

    # Test N = 5
    payload = {"value": 5}
    response = requests.post(url, json=payload, headers=headers, timeout=2)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "computed" in data, f"Response missing 'computed' key: {data}"
    expected = 13.591409
    assert abs(data["computed"] - expected) < 1e-6, f"Expected computed value close to {expected}, got {data['computed']}"