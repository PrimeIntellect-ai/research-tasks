# test_final_state.py
import os
import stat
import time
import requests
import pytest

API_BASE_URL = "http://127.0.0.1:8000"

def wait_for_server(url, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        try:
            requests.get(url, timeout=1)
            return True
        except requests.ConnectionError:
            time.sleep(0.5)
    return False

def test_run_script_exists_and_executable():
    script_path = "/home/user/run.sh"
    assert os.path.exists(script_path), f"Orchestration script missing at {script_path}"
    st = os.stat(script_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"Script {script_path} is not executable"

def test_api_status_endpoint():
    assert wait_for_server(f"{API_BASE_URL}/status"), "API server did not become available"
    response = requests.get(f"{API_BASE_URL}/status", timeout=5)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "frames" in data, f"Response JSON missing 'frames' key: {data}"
    assert data["frames"] == 150, f"Expected 150 frames, got {data['frames']}"

def test_api_execute_endpoint_mul():
    assert wait_for_server(f"{API_BASE_URL}/status"), "API server did not become available"
    payload = {"command": "MUL 7 8"}
    response = requests.post(f"{API_BASE_URL}/execute", json=payload, timeout=5)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "result" in data, f"Response JSON missing 'result' key: {data}"
    assert data["result"] == 56, f"Expected result 56, got {data['result']}"

def test_api_execute_endpoint_add():
    assert wait_for_server(f"{API_BASE_URL}/status"), "API server did not become available"
    payload = {"command": "ADD 100 45"}
    response = requests.post(f"{API_BASE_URL}/execute", json=payload, timeout=5)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "result" in data, f"Response JSON missing 'result' key: {data}"
    assert data["result"] == 145, f"Expected result 145, got {data['result']}"