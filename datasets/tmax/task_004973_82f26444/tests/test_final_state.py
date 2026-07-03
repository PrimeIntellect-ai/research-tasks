# test_final_state.py

import os
import subprocess
import urllib.request
import time
import pytest

def test_nginx_and_services_running():
    # Send a POST request to the Nginx reverse proxy
    url = "http://localhost:8080/upload"
    data = b"test_payload_12345"
    req = urllib.request.Request(url, data=data, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    except Exception as e:
        pytest.fail(f"Failed to communicate with the API via Nginx on port 8080: {e}")

    # Check if the payload reached Redis
    try:
        redis_check = subprocess.run(
            ["redis-cli", "lpop", "data_queue"],
            capture_output=True, text=True, check=True
        )
        assert "test_payload_12345" in redis_check.stdout, "Payload not found in Redis queue. Nginx/Flask integration might be broken."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to check Redis queue: {e}")

def test_validate_data_script():
    script_path = "/home/user/validate_data.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    clean_dir = "/tests/clean"
    evil_dir = "/tests/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run(["python3", script_path, cf], capture_output=True, text=True)
        if res.returncode != 0 or res.stdout.strip() != "ACCEPT":
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        res = subprocess.run(["python3", script_path, ef], capture_output=True, text=True)
        if res.returncode != 1 or res.stdout.strip() != "REJECT":
            evil_failed.append(os.path.basename(ef))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))