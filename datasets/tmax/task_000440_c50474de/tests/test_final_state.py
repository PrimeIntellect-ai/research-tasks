# test_final_state.py

import os
import time
import requests
import pytest

def test_deptool_compiled():
    binary_path = "/app/vendored/deptool/deptool"
    assert os.path.isfile(binary_path), f"The compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"The compiled binary {binary_path} is not executable."

def test_server_script_exists():
    server_script_path = "/app/server.sh"
    assert os.path.isfile(server_script_path), f"The server script {server_script_path} does not exist."
    assert os.access(server_script_path, os.X_OK), f"The server script {server_script_path} is not executable."

def test_http_server_resolve_and_rate_limit():
    url = "http://127.0.0.1:8080/resolve"
    payload = {"file": "src/App.java"}

    # Wait for the next second boundary to ensure we have a fresh second for rate limiting
    time.sleep(1.0 - (time.time() % 1.0))

    # First request
    try:
        response1 = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response1.status_code == 200, f"Expected HTTP 200 for the first request, got {response1.status_code}"
    assert "//app:main" in response1.text, f"Expected '//app:main' in response body, got {response1.text}"

    # Second request
    try:
        response2 = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url} for the second request: {e}")

    assert response2.status_code == 200, f"Expected HTTP 200 for the second request, got {response2.status_code}"
    assert "//app:main" in response2.text, f"Expected '//app:main' in response body, got {response2.text}"

    # Third request (should be rate limited)
    try:
        response3 = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url} for the third request: {e}")

    assert response3.status_code == 429, f"Expected HTTP 429 Too Many Requests for the third request in the same second, got {response3.status_code}"