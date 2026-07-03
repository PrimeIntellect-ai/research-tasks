# test_final_state.py

import os
import requests
import pytest

PORT = 9055
AUTH_TOKEN = "alpha-beta-gamma"
URL = f"http://127.0.0.1:{PORT}/process"

def test_server_pid_exists():
    pid_file = "/home/user/server.pid"
    assert os.path.isfile(pid_file), f"Server PID file {pid_file} does not exist."
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), f"PID file contains non-integer PID: {pid_str}"
    pid = int(pid_str)
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} (from {pid_file}) is not running.")

def test_libalgo_so_built():
    lib_path = "/home/user/c_backend/libalgo.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not built."

def test_http_unauthorized_missing_token():
    try:
        response = requests.post(URL, json={})
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to server at {URL}. Is it running?")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing token, got {response.status_code}. Response: {response.text}"

def test_http_unauthorized_wrong_token():
    headers = {"Authorization": "Bearer wrong-token-123"}
    try:
        response = requests.post(URL, json={}, headers=headers)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to server at {URL}. Is it running?")

    assert response.status_code == 401, f"Expected 401 Unauthorized for wrong token, got {response.status_code}. Response: {response.text}"

def test_http_process_success():
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    payload = {
        "size": 3,
        "weights": [1.5, 2.0, 0.5],
        "matrix": [
            [2.0, 0.0, 0.0],
            [0.0, 3.0, 0.0],
            [0.0, 0.0, 4.0]
        ]
    }
    try:
        response = requests.post(URL, json=payload, headers=headers)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to server at {URL}. Is it running?")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response: {response.text}")

    assert "result" in data, f"Expected 'result' key in JSON response, got {data}"

    expected_result = 11.0
    actual_result = data["result"]
    assert isinstance(actual_result, (int, float)), f"Expected result to be a number, got {type(actual_result)}"
    assert abs(actual_result - expected_result) < 1e-6, f"Expected result {expected_result}, got {actual_result}"