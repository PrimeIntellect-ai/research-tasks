# test_final_state.py

import os
import subprocess
import requests
import pytest

TOKEN = "S3CR3T-AL3RT-T0K3N"
BASE_URL = "http://127.0.0.1:8000"

def test_server_status():
    """Test the /status endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/status", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Alert Dashboard Server on {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()
    assert data.get("tz") == "Europe/Berlin", f"Expected tz 'Europe/Berlin', got {data.get('tz')}"
    assert data.get("locale") == "de_DE.UTF-8", f"Expected locale 'de_DE.UTF-8', got {data.get('locale')}"

def test_server_alert_unauthorized():
    """Test the /alert endpoint without authorization."""
    payload = {"level": "TEST", "message": "Test Message"}
    try:
        response = requests.post(f"{BASE_URL}/alert", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Alert Dashboard Server on {BASE_URL}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for unauthorized request, got {response.status_code}"

def test_server_alert_authorized():
    """Test the /alert endpoint with authorization."""
    payload = {"level": "TEST", "message": "Test Message"}
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.post(f"{BASE_URL}/alert", json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Alert Dashboard Server on {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

def test_server_alerts_get():
    """Test the /alerts endpoint to retrieve stored alerts."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.get(f"{BASE_URL}/alerts", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Alert Dashboard Server on {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), f"Expected response to be a list, got {type(data)}"

    # Check if the previously posted alert is in the list
    expected_alert = {"level": "TEST", "message": "Test Message"}
    assert expected_alert in data, f"Expected {expected_alert} to be in the alerts list, got {data}"

def test_git_bare_repo():
    """Test that /home/user/alerts.git is a bare git repository."""
    repo_path = "/home/user/alerts.git"
    assert os.path.isdir(repo_path), f"Directory {repo_path} does not exist"

    config_path = os.path.join(repo_path, "config")
    assert os.path.isfile(config_path), f"Git config file missing in {repo_path}"

    with open(config_path, "r") as f:
        content = f.read()
    assert "bare = true" in content.lower(), f"Repository at {repo_path} is not configured as bare"

def test_post_receive_hook():
    """Test that the post-receive hook exists and is executable."""
    hook_path = "/home/user/alerts.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"post-receive hook missing at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"post-receive hook at {hook_path} is not executable"

def test_expect_script_exists():
    """Test that the Expect script exists."""
    script_path = "/home/user/auto_alert.exp"
    assert os.path.isfile(script_path), f"Expect script missing at {script_path}"

def test_cron_job():
    """Test that the cron job is configured correctly."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab for user")

    assert "auto_alert.exp" in crontab_content, "auto_alert.exp not found in crontab"

    # Check for every 5 minutes schedule
    # A simple check for */5
    lines = [line for line in crontab_content.splitlines() if not line.strip().startswith("#")]
    found_schedule = False
    for line in lines:
        if "auto_alert.exp" in line and "*/5" in line.split()[0]:
            found_schedule = True
            break

    assert found_schedule, f"Cron job for auto_alert.exp does not seem to be scheduled every 5 minutes. Crontab content: {crontab_content}"