# test_final_state.py

import os
import subprocess
import pytest
import requests
import time
import base64

BASE_URL = "http://127.0.0.1:8080"

def wait_for_server():
    for _ in range(10):
        try:
            requests.get(BASE_URL, timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

def test_server_is_running():
    # Attempt to connect to the server
    # It might not respond to / but it should accept the connection
    try:
        requests.get(f"{BASE_URL}/frame?ts=0.1", timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Server is not listening on 127.0.0.1:8080")

def test_frame_endpoint():
    response = requests.get(f"{BASE_URL}/frame?ts=2.0", timeout=5)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /frame is not valid JSON")

    assert "time" in data, "JSON response missing 'time' key"
    assert "image" in data, "JSON response missing 'image' key"

    # Verify base64
    try:
        decoded = base64.b64decode(data["image"])
        assert len(decoded) > 0, "Decoded image is empty"
    except Exception:
        pytest.fail("Image data is not valid base64")

def test_logs_endpoint_valid_json():
    # Make a couple of requests to generate logs
    requests.get(f"{BASE_URL}/frame?ts=1.0", timeout=2)
    requests.get(f"{BASE_URL}/frame?ts=1.5", timeout=2)

    # Query logs with large timestamps to test 32-bit overflow fix
    start_ts = 2147483647000
    end_ts = 2147484000000

    response = requests.get(f"{BASE_URL}/logs?start={start_ts}&end={end_ts}", timeout=5)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        logs = response.json()
    except ValueError:
        pytest.fail("Response from /logs is not valid JSON. The JSON serialization issue might not be fixed.")

    assert isinstance(logs, list), "Expected logs to be a JSON array"

def test_regression_test_script():
    script_path = "/home/user/app/regression_test.sh"
    assert os.path.exists(script_path), f"Regression test script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Regression test script {script_path} is not executable"

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Regression test script failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"