# test_final_state.py

import os
import time
import requests
import pytest

APP_DIR = "/home/user/app"
BASHRC_PATH = "/home/user/.bashrc"
START_SCRIPT = os.path.join(APP_DIR, "start_all.sh")

def test_bashrc_env_vars():
    """Verify that required environment variables are exported in .bashrc."""
    assert os.path.isfile(BASHRC_PATH), f"{BASHRC_PATH} does not exist."
    with open(BASHRC_PATH, "r") as f:
        content = f.read()

    assert "FINOPS_API_KEY=opt-cost-2024" in content or "FINOPS_API_KEY=\"opt-cost-2024\"" in content or "FINOPS_API_KEY='opt-cost-2024'" in content, "FINOPS_API_KEY is not correctly set in .bashrc"
    assert "DATASTORE_HOST" in content, "DATASTORE_HOST is not set in .bashrc"
    assert "DATASTORE_PORT" in content, "DATASTORE_PORT is not set in .bashrc"

def test_start_script_exists_and_executable():
    """Verify that start_all.sh exists, is executable, and contains a monitoring loop."""
    assert os.path.isfile(START_SCRIPT), f"{START_SCRIPT} does not exist."
    assert os.access(START_SCRIPT, os.X_OK), f"{START_SCRIPT} is not executable."

    with open(START_SCRIPT, "r") as f:
        content = f.read()

    # Check for some form of loop for process monitoring
    assert "while" in content or "until" in content, f"{START_SCRIPT} does not seem to contain a monitoring loop."

def test_api_endpoint():
    """Verify that the end-to-end API works via Nginx reverse proxy."""
    url = "http://localhost:8080/api/v1/costs"

    # Retry mechanism to allow services to be fully up if they were just started
    max_retries = 5
    response = None
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)

    assert response is not None, f"Failed to connect to {url}"
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("status") == "optimized", f"Expected status 'optimized', got {data.get('status')}"
    assert "data" in data, "Response JSON missing 'data' key"
    assert data["data"].get("cloud_cost") == 420.50, f"Expected cloud_cost 420.50, got {data['data'].get('cloud_cost')}"