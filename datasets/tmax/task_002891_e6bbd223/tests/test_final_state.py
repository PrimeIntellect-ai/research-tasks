# test_final_state.py
import os
import time
import requests
import re
import pytest

PORT = 8088
URL = f"http://127.0.0.1:{PORT}"
SECRET = "R0ll0ut_S3cr3t"
UPSTREAM = "127.0.0.1:9099"

def test_proxy_auth_missing():
    """Test that requests without the X-Deploy-Auth header return 401 Unauthorized."""
    try:
        resp = requests.get(f"{URL}/test1", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy: {e}")
    assert resp.status_code == 401, f"Expected 401 Unauthorized for missing auth, got {resp.status_code}"

def test_proxy_auth_wrong():
    """Test that requests with an incorrect X-Deploy-Auth header return 401 Unauthorized."""
    try:
        resp = requests.get(f"{URL}/test2", headers={"X-Deploy-Auth": "WrongKey"}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy: {e}")
    assert resp.status_code == 401, f"Expected 401 Unauthorized for wrong auth, got {resp.status_code}"

def test_proxy_auth_correct():
    """Test that requests with the correct X-Deploy-Auth header return 200 OK and the correct JSON payload."""
    try:
        resp = requests.get(f"{URL}/target", headers={"X-Deploy-Auth": SECRET}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy: {e}")
    assert resp.status_code == 200, f"Expected 200 OK for correct auth, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Response was not valid JSON")

    assert data.get("status") == "routed", f"Expected status 'routed', got {data.get('status')}"
    assert data.get("upstream") == UPSTREAM, f"Expected upstream '{UPSTREAM}', got {data.get('upstream')}"

def test_log_rotation_and_format():
    """Test that the log rotation daemon works and logs are formatted correctly."""
    # Make 6 rapid requests to trigger log rotation
    for i in range(6):
        try:
            requests.get(f"{URL}/rot_test_{i}", headers={"X-Deploy-Auth": SECRET}, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to proxy during log rotation test: {e}")

    # Wait for log rotation daemon to run (runs every 2 seconds)
    time.sleep(3.5)

    archive_path = "/home/user/archive/access.log.1"
    access_log_path = "/home/user/access.log"

    assert os.path.exists(archive_path), f"Log archive {archive_path} does not exist after rotation. Ensure the daemon is running and rotating files > 5 lines."

    with open(archive_path, "r") as f:
        archived_lines = [line for line in f.read().split("\n") if line.strip()]

    assert len(archived_lines) >= 5, f"Expected at least 5 lines in {archive_path}, got {len(archived_lines)}"

    # Check log format
    # Format: [YYYY-MM-DD HH:MM:SS] | X-Deploy-Auth: <header_value_or_NONE> | Path: <request_path>
    log_pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] \| X-Deploy-Auth: .* \| Path: /.*$")
    for line in archived_lines:
        assert log_pattern.match(line), f"Log line does not match expected format: {line}"

    assert os.path.exists(access_log_path), f"Access log {access_log_path} does not exist"

    with open(access_log_path, "r") as f:
        access_lines = [line for line in f.read().split("\n") if line.strip()]

    for line in access_lines:
        assert log_pattern.match(line), f"Log line does not match expected format: {line}"