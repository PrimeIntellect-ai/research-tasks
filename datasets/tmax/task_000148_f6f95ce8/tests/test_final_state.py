# test_final_state.py

import os
import subprocess
import requests
import pytest
import time

def test_gateway_data_dir_exists():
    data_dir = "/home/user/gateway_data"
    assert os.path.exists(data_dir), f"Directory {data_dir} does not exist."
    assert os.path.isdir(data_dir), f"{data_dir} is not a directory."

def test_health_check_script_exists_and_runs():
    script_path = "/home/user/health_check.sh"
    assert os.path.exists(script_path), f"Health check script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Run the health check script and assert it exits with 0
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Health check script failed with exit code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

def test_telemetry_gateway_http_endpoint():
    url = "http://127.0.0.1:8443/status"
    headers = {
        "Authorization": "Bearer admin-secret-991"
    }

    # Try connecting a few times in case the service is slow to respond
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=2)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            if attempt == max_retries - 1:
                pytest.fail(f"Failed to connect to {url} after {max_retries} attempts. Is the service running and bound to 127.0.0.1:8443?")
            time.sleep(1)

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"