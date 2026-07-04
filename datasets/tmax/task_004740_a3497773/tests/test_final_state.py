# test_final_state.py
import os
import requests
import pytest
import time

def wait_for_port(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(url, timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    return False

def test_service_eval_addition():
    url = "http://127.0.0.1:8080/eval?expr=20%2B22"
    wait_for_port("http://127.0.0.1:8080/")

    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP service: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data == {"result": 42}, f"Expected {{'result': 42}}, got {data}"

def test_service_eval_subtraction():
    url = "http://127.0.0.1:8080/eval?expr=100-50"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP service: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data == {"result": 50}, f"Expected {{'result': 50}}, got {data}"

def test_service_eval_buffer_overflow_protection():
    long_expr = "9" * 200
    url = f"http://127.0.0.1:8080/eval?expr={long_expr}"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Service crashed or failed to respond on long input (possible segfault): {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data == {"error": "Invalid"}, f"Expected {{'error': 'Invalid'}}, got {data}"

def test_hypothesis_test_file_exists_and_contains_keywords():
    test_file_path = "/home/user/test_expr.py"
    assert os.path.isfile(test_file_path), f"Test file {test_file_path} is missing."

    with open(test_file_path, "r") as f:
        content = f.read()

    assert "hypothesis" in content, f"Keyword 'hypothesis' not found in {test_file_path}"
    assert "strategies.text" in content or "text(" in content, f"Keyword 'strategies.text' (or similar) not found in {test_file_path}"

def test_shared_library_built():
    so_path = "/app/vendor/libexpr/libexpr.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not built. Fix the Makefile."