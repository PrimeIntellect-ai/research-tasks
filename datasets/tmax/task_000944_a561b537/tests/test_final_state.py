# test_final_state.py

import os
import stat
import json
import pytest
import requests

def test_deploy_script_exists():
    """Check if the deployment script was created."""
    deploy_script = "/home/user/deploy.py"
    assert os.path.isfile(deploy_script), f"Deploy script {deploy_script} is missing."

def test_storage_dir_permissions():
    """Check if the target storage directory exists and has 0755 permissions."""
    target_dir = "/home/user/app_data/storage"
    assert os.path.isdir(target_dir), f"Target directory {target_dir} is missing."

    st = os.stat(target_dir)
    permissions = oct(st.st_mode & 0o777)
    assert permissions == '0o755', f"Expected permissions 0o755 for {target_dir}, but got {permissions}."

def test_service_running_and_writing():
    """Test the service via HTTP and verify filesystem state."""
    base_url = "http://127.0.0.1:9090"
    headers = {"Authorization": "Bearer DeployMagic99"}
    payload = {"data": "healthcheck_123"}

    # 1. POST request to write data
    try:
        r_post = requests.post(f"{base_url}/write", json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {base_url}/write: {e}")

    assert r_post.status_code == 200, f"Expected 200 OK for POST /write, got {r_post.status_code}. Response: {r_post.text}"

    # 2. GET request to read data
    try:
        r_get = requests.get(f"{base_url}/read", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {base_url}/read: {e}")

    assert r_get.status_code == 200, f"Expected 200 OK for GET /read, got {r_get.status_code}. Response: {r_get.text}"

    try:
        response_json = r_get.json()
    except ValueError:
        pytest.fail(f"Response from GET /read is not valid JSON: {r_get.text}")

    assert response_json.get("data") == "healthcheck_123", f"Expected data 'healthcheck_123' in GET /read response, got {response_json}"

    # 3. Check the filesystem to ensure state.json contains the written data
    state_file = "/home/user/app_data/storage/state.json"
    assert os.path.isfile(state_file), f"State file {state_file} was not created. The service might still be writing to the wrong location."

    with open(state_file, "r") as f:
        try:
            file_data = json.load(f)
        except ValueError:
            pytest.fail(f"State file {state_file} does not contain valid JSON.")

    assert file_data.get("data") == "healthcheck_123", f"Expected data 'healthcheck_123' in {state_file}, got {file_data}"