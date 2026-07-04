# test_final_state.py

import os
import requests
import pytest
import time

def wait_for_server(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Just check if the port is open and responding, even if GET is not allowed
            requests.get(url, timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

def test_rust_binary_exists():
    binary_path = "/app/calculator/target/release/calculator"
    assert os.path.isfile(binary_path), f"Compiled Rust binary not found at {binary_path}. Did you compile in release mode?"

def test_http_server_calculate_endpoint():
    base_url = "http://127.0.0.1:8888"
    endpoint = f"{base_url}/calculate"

    server_up = wait_for_server(base_url, timeout=5)
    assert server_up, f"Could not connect to HTTP server at {base_url}"

    # Test case 1: positive number
    payload = {"number": 4}
    try:
        resp = requests.post(endpoint, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"POST request to {endpoint} failed: {e}")

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {resp.text}")

    assert "result" in data, f"Expected 'result' key in JSON response, got: {data}"
    assert data["result"] == 420, f"Expected result 420 for input 4, got {data['result']}"

    # Test case 2: negative number
    payload = {"number": -2}
    try:
        resp = requests.post(endpoint, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"POST request to {endpoint} failed: {e}")

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}"
    data = resp.json()
    assert data["result"] == -210, f"Expected result -210 for input -2, got {data['result']}"

    # Test case 3: zero
    payload = {"number": 0}
    try:
        resp = requests.post(endpoint, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"POST request to {endpoint} failed: {e}")

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}"
    data = resp.json()
    assert data["result"] == 0, f"Expected result 0 for input 0, got {data['result']}"