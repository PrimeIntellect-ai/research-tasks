# test_final_state.py

import os
import requests
import pytest

MAGIC_NUMBER = 145

def test_server_pid_exists():
    """Verify that the server PID file exists and the process is running."""
    pid_file = "/home/user/server.pid"
    assert os.path.exists(pid_file), f"PID file missing: {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: '{pid_str}'"
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

def test_shared_library_exists():
    """Verify that the compiled shared library exists."""
    lib_path = "/home/user/libdeploy.so"
    assert os.path.exists(lib_path), f"Shared library missing: {lib_path} does not exist."
    assert os.path.isfile(lib_path), f"Shared library is not a file: {lib_path}."

def test_api_status():
    """Verify the /status endpoint returns the correct magic number."""
    url = "http://127.0.0.1:8000/status"
    try:
        response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response: {response.text}")

    assert data.get("status") == "ready", f"Expected status 'ready', got '{data.get('status')}'"
    assert data.get("magic") == MAGIC_NUMBER, f"Expected magic {MAGIC_NUMBER}, got {data.get('magic')}"

def test_api_compute():
    """Verify the /compute endpoint correctly loads the library and computes the offset."""
    test_cases = [
        (10, 155),
        (-45, 100)
    ]

    for val, expected_result in test_cases:
        url = f"http://127.0.0.1:8000/compute/{val}"
        try:
            response = requests.get(url, timeout=2)
        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to {url}: {e}")

        assert response.status_code == 200, f"Expected HTTP 200 for {url}, got {response.status_code}. Response: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response from {url} is not valid JSON. Response: {response.text}")

        assert "result" in data, f"Key 'result' missing in response from {url}. Response: {data}"
        assert data["result"] == expected_result, f"Expected result {expected_result} for input {val}, got {data['result']}"