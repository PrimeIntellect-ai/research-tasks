# test_final_state.py
import os
import requests
import pytest

def test_libchecksum_exists():
    """Test that the shared library exists."""
    assert os.path.isfile("/home/user/libchecksum.so"), "The shared library /home/user/libchecksum.so is missing."

def test_benchmark_log_exists():
    """Test that the benchmark log exists and is not empty."""
    log_path = "/home/user/benchmark.log"
    assert os.path.isfile(log_path), f"The benchmark log is missing: {log_path}"
    assert os.path.getsize(log_path) > 0, f"The benchmark log is empty: {log_path}"

def test_health_endpoint():
    """Test the /health endpoint via the reverse proxy."""
    try:
        response = requests.get("http://127.0.0.1:9000/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the reverse proxy or backend for /health: {e}")

    assert response.status_code == 200, f"Expected 200 OK for /health, got {response.status_code}"
    assert response.text.strip() == "OK", f"Expected body 'OK' for /health, got '{response.text}'"

def test_process_endpoint_unauthorized():
    """Test the /process endpoint with an invalid token."""
    headers = {"Authorization": "Bearer invalid-token"}
    try:
        response = requests.post("http://127.0.0.1:9000/process", headers=headers, data="test", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the reverse proxy or backend for /process: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid token, got {response.status_code}"

def test_process_endpoint_authorized():
    """Test the /process endpoint with the valid token and check the checksum result."""
    headers = {"Authorization": "Bearer gamma-ray-burst"}
    body = "test"
    try:
        response = requests.post("http://127.0.0.1:9000/process", headers=headers, data=body, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the reverse proxy or backend for /process: {e}")

    assert response.status_code == 200, f"Expected 200 OK for valid token, got {response.status_code}"
    assert response.text.strip() == "17", f"Expected body '17' for input 'test', got '{response.text}'"