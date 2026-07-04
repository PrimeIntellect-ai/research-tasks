# test_final_state.py

import os
import glob
import requests
import pytest

def test_directories_exist():
    """Check that the required directories have been created."""
    dirs = [
        "/home/user/config.git",
        "/home/user/active_configs",
        "/home/user/backups",
        "/home/user/workspace"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Required directory {d} does not exist."

def test_git_hook_exists():
    """Check that the post-receive git hook exists and is executable."""
    hook_path = "/home/user/config.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Git hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Git hook {hook_path} is not executable."

def test_supervisor_script_exists():
    """Check that the supervisor script exists and is executable."""
    supervisor_path = "/home/user/supervisor.sh"
    assert os.path.isfile(supervisor_path), f"Supervisor script {supervisor_path} does not exist."
    assert os.access(supervisor_path, os.X_OK), f"Supervisor script {supervisor_path} is not executable."

def test_deployed_files_exist():
    """Check that the application files were successfully deployed to active_configs."""
    nginx_conf = "/home/user/active_configs/nginx.conf"
    backend_sh = "/home/user/active_configs/backend.sh"
    assert os.path.isfile(nginx_conf), f"Deployed Nginx config {nginx_conf} does not exist."
    assert os.path.isfile(backend_sh), f"Deployed backend script {backend_sh} does not exist."

def test_backup_created():
    """Check that at least one backup tarball was created in the backups directory."""
    backups = glob.glob("/home/user/backups/config-*.tar.gz")
    assert len(backups) > 0, "No backup tarball found in /home/user/backups/ matching config-<UNIX_TIMESTAMP>.tar.gz."

def test_http_endpoint_transcription():
    """Verify that the HTTP endpoint serves the expected transcription."""
    url = "http://127.0.0.1:8080/transcribe"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"HTTP request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected HTTP status code 200, got {response.status_code}. Response: {response.text}"

    body = response.text.strip()
    expected_transcript = "ECHO BRAVO CHARLIE ABORT SEQUENCE"
    assert expected_transcript in body, f"Expected transcript '{expected_transcript}' not found in response body. Got: '{body}'"