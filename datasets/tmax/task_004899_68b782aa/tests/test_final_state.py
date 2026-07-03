# test_final_state.py
import os
import time
import requests
import pytest

def test_status_file():
    """Check that the agent wrote SERVICE_READY to status.txt"""
    status_file = "/home/user/status.txt"
    assert os.path.isfile(status_file), f"Status file missing: {status_file}"
    with open(status_file, "r") as f:
        content = f.read().strip()
    assert content == "SERVICE_READY", f"Expected 'SERVICE_READY' in {status_file}, got '{content}'"

def test_webhook_and_deployment_log():
    """Test the webhook endpoint and verify that the deployment log is created."""
    url = "http://127.0.0.1:8080/api/v1/deploy"
    headers = {
        "Authorization": "Bearer DeployerToken-99x",
        "Content-Type": "application/json"
    }
    payload = {
        "service": "frontend",
        "strategy": "rolling"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the webhook service at {url}: {e}")

    assert response.status_code in (200, 202), f"Expected status 200 or 202, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response was not valid JSON")

    assert data.get("status") == "deployment_started", f"Expected status 'deployment_started', got {data.get('status')}"

    # Wait for the background job to write the log
    log_file = "/home/user/deploy_logs/frontend_deployment.log"

    max_retries = 10
    for _ in range(max_retries):
        if os.path.isfile(log_file):
            break
        time.sleep(0.5)

    assert os.path.isfile(log_file), f"Deployment log file was not created at {log_file} after triggering the webhook."

    # Optional: check if the file has content
    assert os.path.getsize(log_file) > 0, f"Deployment log file {log_file} is empty."