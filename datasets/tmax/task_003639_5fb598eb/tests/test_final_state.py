# test_final_state.py

import os
import pytest
import requests
import time

def test_server_pid_file_exists():
    pid_file = "/home/user/server.pid"
    assert os.path.isfile(pid_file), f"Missing PID file: {pid_file}"
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), f"PID file does not contain a valid integer: {pid_str}"

def test_api_solve_request_1():
    url = "http://127.0.0.1:8080/solve?target=100&w=10,15,25"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected = {"status": "success", "result": 50}
    assert data == expected, f"Expected {expected}, got {data}"

def test_api_solve_request_2():
    url = "http://127.0.0.1:8080/solve?target=10&w=2,3"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected = {"status": "success", "result": 5}
    assert data == expected, f"Expected {expected}, got {data}"