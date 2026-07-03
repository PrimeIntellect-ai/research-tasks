# test_final_state.py

import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8080"

def wait_for_server(timeout=5):
    """Wait for the HTTP server to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(f"{BASE_URL}/status")
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    return False

def test_server_is_running():
    assert wait_for_server(), "The Rust HTTP server is not running or not reachable on 127.0.0.1:8080."

def test_config_max_connections():
    response = requests.get(f"{BASE_URL}/config/max_connections")
    assert response.status_code == 200, f"Expected 200 OK for max_connections, got {response.status_code}"

    data = response.json()
    assert data.get("key") == "max_connections", f"Expected key 'max_connections', got {data.get('key')}"
    assert data.get("value") == 2048, f"Expected value 2048 for max_connections, got {data.get('value')}"

def test_config_timeout():
    response = requests.get(f"{BASE_URL}/config/timeout")
    assert response.status_code == 404, f"Expected 404 Not Found for timeout, got {response.status_code}"

def test_status_endpoint():
    response = requests.get(f"{BASE_URL}/status")
    assert response.status_code == 200, f"Expected 200 OK for /status, got {response.status_code}"

    data = response.json()
    assert data.get("files_processed") == 3, f"Expected 3 files processed, got {data.get('files_processed')}"