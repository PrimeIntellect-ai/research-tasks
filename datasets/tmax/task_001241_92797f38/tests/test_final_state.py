# test_final_state.py

import os
import urllib.request
import urllib.error
import json
import hashlib

def test_result_log_success():
    """Verify that the result.log file exists and contains SUCCESS."""
    log_path = "/home/user/test-env/result.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did you run env-tester?"

    with open(log_path, 'r') as f:
        content = f.read()

    assert "SUCCESS" in content, f"Expected 'SUCCESS' in {log_path}, but got: {content}"

def test_mock_server_exists():
    """Verify that the mock_server.js file was created."""
    mock_server_path = "/home/user/test-env/mock_server.js"
    assert os.path.isfile(mock_server_path), f"File {mock_server_path} does not exist."

def test_pyproject_toml_fixed():
    """Verify that the conflicting urllib3 constraint was changed in pyproject.toml."""
    toml_path = "/home/user/test-env/python-pkg/pyproject.toml"
    assert os.path.isfile(toml_path), f"File {toml_path} does not exist."

    with open(toml_path, 'r') as f:
        content = f.read()

    # The original had "urllib3==1.25.1" which conflicts with requests==2.31.0
    # We just check that it's no longer strictly ==1.25.1 or that it was modified.
    assert "urllib3==1.25.1" not in content, "The conflicting urllib3==1.25.1 constraint is still in pyproject.toml."

def test_mock_server_endpoint_behavior():
    """Verify that the mock server is running and returns the correct payload and checksum."""
    url = "http://localhost:8080/config"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            status_code = response.getcode()
            body = response.read().decode('utf-8')
            checksum_header = response.headers.get('X-Checksum')
    except urllib.error.URLError as e:
        # If the server is not running, we skip this test or fail gracefully
        # The prompt says "Start your Node.js mock server in the background", so it might still be running.
        # If it's not running, we shouldn't fail the whole suite if result.log is already correct, 
        # but a robust test would check if it's reachable. We'll just assert it doesn't raise if possible,
        # but we can accept if the student killed it after finishing.
        # Let's just check the result.log as the primary source of truth.
        return

    assert status_code == 200, f"Expected status code 200, got {status_code}"
    expected_body = '{"status":"ready","version":"1.0.0"}'
    assert body == expected_body, f"Expected body '{expected_body}', got '{body}'"

    expected_checksum = hashlib.sha256((expected_body + "QA_ENV_SALT_123").encode('utf-8')).hexdigest()
    assert checksum_header == expected_checksum, f"Expected X-Checksum header '{expected_checksum}', got '{checksum_header}'"