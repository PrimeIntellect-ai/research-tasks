# test_final_state.py

import os
import shutil
import pytest
import requests

def test_bash_profile_env_var():
    path = "/home/user/.bash_profile"
    assert os.path.exists(path), f"Missing {path}"
    with open(path, "r") as f:
        content = f.read()

    # Check if DEPLOY_ENVIRONMENT is exported as production
    has_env = (
        "DEPLOY_ENVIRONMENT=production" in content or 
        "DEPLOY_ENVIRONMENT='production'" in content or 
        'DEPLOY_ENVIRONMENT="production"' in content
    )
    assert has_env, "DEPLOY_ENVIRONMENT=production is not set in .bash_profile"

def test_deploy_data_disk_space():
    path = "/home/user/deploy_data"
    assert os.path.exists(path), f"Missing {path}"
    total, used, free = shutil.disk_usage(path)
    assert free > 0, f"Disk space at {path} is still completely full. Free space: {free} bytes."

def test_service_unauthorized():
    url = "http://127.0.0.1:8085/version"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}. Is it running? Error: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

def test_service_authorized():
    url = "http://127.0.0.1:8085/version"
    headers = {"Authorization": "Bearer secret99"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected 200 OK with correct token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert data.get("version") == "v2", f"Expected version 'v2', got {data.get('version')}"