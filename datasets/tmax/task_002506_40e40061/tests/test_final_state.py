# test_final_state.py

import os
import stat
import urllib.request
import urllib.error
import pytest

def test_deploy_script_exists_and_executable():
    """Verify /home/user/deploy.sh exists and is executable."""
    script_path = '/home/user/deploy.sh'
    assert os.path.exists(script_path), f"Deployment script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deployment script {script_path} is not executable."

def get_expected_token():
    """Helper to extract the expected token from service_config.txt."""
    config_path = '/home/user/service_config.txt'
    assert os.path.exists(config_path), f"Configuration file {config_path} does not exist."

    with open(config_path, 'r') as f:
        content = f.read().strip()

    for line in content.splitlines():
        if line.startswith("TOKEN="):
            return line.split("=", 1)[1].strip()

    pytest.fail(f"Could not find 'TOKEN=' in {config_path}.")

def test_service_config_generated():
    """Verify service_config.txt was generated and contains a token."""
    token = get_expected_token()
    assert token, "Token value is empty."

def test_rust_server_status_response():
    """Verify the Rust server is running on port 8443 and returns the correct token."""
    expected_token = get_expected_token()
    url = "http://127.0.0.1:8443/status"

    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200 OK, got {response.status}"
            body = response.read().decode('utf-8').strip()
            assert body == expected_token, f"Expected token '{expected_token}', but got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the Rust server at {url}: {e}")

def test_deploy_success_log():
    """Verify deploy_success.log exists and contains the correct exact message."""
    expected_token = get_expected_token()
    log_path = '/home/user/deploy_success.log'

    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_content = f"Rollout complete. Active token: {expected_token}"
    assert content == expected_content, f"Log file content mismatch. Expected '{expected_content}', got '{content}'"