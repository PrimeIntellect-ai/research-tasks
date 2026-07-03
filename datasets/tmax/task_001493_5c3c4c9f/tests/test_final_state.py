# test_final_state.py

import os
import time
import requests
import pytest

def test_libcsched_built():
    """Verify that the shared library was successfully built."""
    lib_path = "/home/user/app/vendor/libcsched/libcsched.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist. Did you fix the Makefile and build it?"

def test_c_code_fixed():
    """Verify that the off-by-one bug in schedule.c was fixed."""
    c_file = "/home/user/app/vendor/libcsched/schedule.c"
    assert os.path.isfile(c_file), f"Source file {c_file} is missing."
    with open(c_file, "r") as f:
        content = f.read()
        assert "i <= num_tasks" not in content, "The out-of-bounds bug (i <= num_tasks) in schedule.c is still present."

def test_server_pid_exists():
    """Verify that the server.pid file exists."""
    pid_file = "/home/user/app/server.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing. Did you save the server PID?"

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer."

def test_api_unauthorized():
    """Verify that the API rejects unauthorized requests with 401."""
    url = "http://127.0.0.1:8080/schedule"
    payload = {"tasks": [10, 20, 30]}

    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for request without auth header, got {response.status_code}"

def test_api_authorized_and_correct():
    """Verify that the API returns the correct schedule for an authorized request."""
    url = "http://127.0.0.1:8080/schedule"
    payload = {"tasks": [10, 20, 30]}
    headers = {
        "Authorization": "Bearer RM-DEPLOY-999",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK for authorized request, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "schedule" in data, f"Response JSON missing 'schedule' key: {data}"
    expected_schedule = [0, 10, 30]
    assert data["schedule"] == expected_schedule, f"Expected schedule {expected_schedule}, got {data['schedule']}"