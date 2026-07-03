# test_final_state.py

import os
import requests
import pytest
import time

def test_backup_service_go_exists():
    assert os.path.isfile("/home/user/backup_service.go"), "The Go source file /home/user/backup_service.go is missing."

def test_restore_endpoint():
    url = "http://127.0.0.1:8080/restore"
    payload = {"repo_name": "test_repo"}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go web service on {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}. Response text: {response.text}")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("owner") == "admin_user", f"Expected owner 'admin_user', got {data.get('owner')}"
    assert "INTEGRITY_CHECK_PASSED" in data.get("validator_output", ""), f"Expected validator_output to contain 'INTEGRITY_CHECK_PASSED', got {data.get('validator_output')}"

def test_restored_directory_and_hook():
    repo_dir = "/home/user/restored/test_repo"
    assert os.path.isdir(repo_dir), f"Restored repository directory {repo_dir} is missing. The service did not extract the archive properly."

    manifest_path = os.path.join(repo_dir, "manifest.txt")
    assert os.path.isfile(manifest_path), f"manifest.txt is missing in the restored repository."

    hook_path = os.path.join(repo_dir, "hooks", "pre-receive")
    assert os.path.isfile(hook_path), f"pre-receive hook is missing at {hook_path}."
    assert os.access(hook_path, os.X_OK), f"pre-receive hook at {hook_path} is not executable."