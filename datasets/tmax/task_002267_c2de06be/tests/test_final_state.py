# test_final_state.py

import os
import time
import glob
import json
import stat
import requests
import pytest

def test_telemetry_server():
    """Verify that the daemon responds to GET /api/v1/fault with the expected JSON payload."""
    url = "http://127.0.0.1:8080/api/v1/fault"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the telemetry server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response body is not valid JSON. Body: {response.text}")

    expected_data = {"faulty_ip": "10.0.40.55", "log_status": "active"}
    assert data == expected_data, f"Expected JSON payload {expected_data}, got {data}"

def test_log_rotation_and_permissions():
    """Verify that the daemon rotates the log file when it exceeds 500 bytes and sets permissions to 0444."""
    log_dir = "/home/user/net_logs"
    archive_dir = os.path.join(log_dir, "archive")
    log_file = os.path.join(log_dir, "traffic.log")

    # Ensure directories exist
    os.makedirs(archive_dir, exist_ok=True)

    # Record existing archive files to distinguish the new one
    existing_archives = set(glob.glob(os.path.join(archive_dir, "traffic_*.log")))

    # Write 600 bytes of dummy data to traffic.log
    with open(log_file, "w") as f:
        f.write("A" * 600)

    # Wait for the daemon to detect and rotate
    time.sleep(2)

    # Verify traffic.log is either gone or smaller than 500 bytes
    if os.path.exists(log_file):
        assert os.path.getsize(log_file) <= 500, f"Log file was not rotated, size is still {os.path.getsize(log_file)} bytes"

    # Check for the new archive file
    current_archives = set(glob.glob(os.path.join(archive_dir, "traffic_*.log")))
    new_archives = current_archives - existing_archives

    assert len(new_archives) >= 1, "No new archive file was created in the archive directory."

    # Check permissions of the newly created archive file(s)
    for archive in new_archives:
        file_stat = os.stat(archive)
        permissions = stat.S_IMODE(file_stat.st_mode)
        assert permissions == 0o444, f"Expected permissions 0444 for {archive}, got {oct(permissions)}"