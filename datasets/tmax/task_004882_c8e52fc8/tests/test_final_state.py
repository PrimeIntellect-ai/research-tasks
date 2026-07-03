# test_final_state.py

import os
import json
import time
import subprocess
import requests
import pytest

@pytest.fixture(scope="module", autouse=True)
def start_api_service():
    """Run the user's startup script and wait for the API to become available."""
    script_path = "/home/user/start_services.sh"
    assert os.path.isfile(script_path), f"Startup script {script_path} not found."

    # Execute the startup script
    subprocess.run(["bash", script_path], check=True)

    # Wait for the service to listen on port 5000
    service_up = False
    for _ in range(20):
        try:
            # We just need to check if the port is open and responding to HTTP
            requests.get("http://127.0.0.1:5000/api/v1/data", timeout=1)
            service_up = True
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)

    assert service_up, "API Gateway did not start on 127.0.0.1:5000 within the timeout."

    yield

    # Cleanup using the PID file if it exists
    pid_file = "/home/user/api.pid"
    if os.path.isfile(pid_file):
        try:
            with open(pid_file, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, 9)
        except (ValueError, ProcessLookupError, OSError):
            pass

def test_data_mount_config():
    """Verify the storage setup and config.json content."""
    config_path = "/home/user/data_mount/config.json"
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."

    with open(config_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {config_path} does not contain valid JSON.")

    expected_data = {"status": "migrated", "version": "1.0"}
    assert data == expected_data, f"Config JSON content mismatch. Expected {expected_data}, got {data}"

def test_adapter_exists():
    """Verify the adapter module exists."""
    assert os.path.isfile("/app/adapter.py"), "Adapter script /app/adapter.py does not exist."

def test_api_auth_failure():
    """Verify that the API returns 401 Unauthorized when the token is missing or incorrect."""
    url = "http://127.0.0.1:5000/api/v1/data"

    # Missing header
    response = requests.get(url)
    assert response.status_code == 401, f"Expected 401 for missing auth, got {response.status_code}"

    # Incorrect header
    headers = {"Authorization": "Bearer wrong-token"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 401, f"Expected 401 for incorrect auth, got {response.status_code}"

def test_api_success():
    """Verify that the API returns 200 OK and the correct data when authenticated."""
    url = "http://127.0.0.1:5000/api/v1/data"
    headers = {"Authorization": "Bearer migrate-token-99"}

    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        response_data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"API response is not valid JSON. Response text: {response.text}")

    expected_response = {
        "source": "legacy",
        "data": {
            "status": "migrated",
            "version": "1.0"
        }
    }
    assert response_data == expected_response, f"API response data mismatch. Expected {expected_response}, got {response_data}"