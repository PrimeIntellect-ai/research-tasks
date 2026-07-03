# test_final_state.py

import os
import requests
import pytest
import time

API_BASE_URL = "http://127.0.0.1:8000"

def wait_for_server(url, timeout=5):
    """Wait for the server to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(url)
            return True
        except requests.ConnectionError:
            time.sleep(0.5)
    return False

@pytest.fixture(scope="module", autouse=True)
def setup_server():
    assert wait_for_server(f"{API_BASE_URL}/result/101"), "API server is not reachable at 127.0.0.1:8000"

def test_api_result_101():
    response = requests.get(f"{API_BASE_URL}/result/101")
    assert response.status_code == 200, f"Expected status 200 for ID 101, got {response.status_code}"
    data = response.json()
    assert data.get("id") == 101, f"Expected id 101, got {data.get('id')}"
    assert data.get("result") == -38.0, f"Expected result -38.0, got {data.get('result')}"

def test_api_result_102():
    response = requests.get(f"{API_BASE_URL}/result/102")
    assert response.status_code == 200, f"Expected status 200 for ID 102, got {response.status_code}"
    data = response.json()
    assert data.get("id") == 102, f"Expected id 102, got {data.get('id')}"
    assert data.get("result") == -37.0, f"Expected result -37.0, got {data.get('result')}"

def test_api_result_103():
    response = requests.get(f"{API_BASE_URL}/result/103")
    assert response.status_code == 200, f"Expected status 200 for ID 103, got {response.status_code}"
    data = response.json()
    assert data.get("id") == 103, f"Expected id 103, got {data.get('id')}"
    assert data.get("result") == -30.0, f"Expected result -30.0, got {data.get('result')}"

def test_api_result_not_found():
    response = requests.get(f"{API_BASE_URL}/result/999")
    assert response.status_code == 404, f"Expected status 404 for ID 999, got {response.status_code}"

def test_pipeline_log_exists_and_contains_data():
    log_path = "/app/pipeline.log"
    assert os.path.exists(log_path), f"Log file not found at {log_path}"
    assert os.path.isfile(log_path), f"Path {log_path} is not a file"

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert len(content.strip()) > 0, "Log file is empty"
        # Check for standard logging format loosely
        assert "-" in content and ":" in content, "Log file does not appear to use a standard logging format"