# test_final_state.py

import hashlib
import os
import time
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
BENIGN_PAYLOAD = b"BENIGN_PAYLOAD_1"
MALICIOUS_PAYLOAD = b"MALICIOUS_PAYLOAD_1"

@pytest.fixture(scope="module", autouse=True)
def wait_for_service():
    """Wait for the Go service to become available before running tests."""
    for _ in range(30):
        try:
            # We use /audit as a health check endpoint since it should be implemented
            requests.get(f"{BASE_URL}/audit", timeout=1)
            return
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    pytest.fail("Service on port 8080 is not responding within the timeout.")

def test_directories_exist():
    assert os.path.isdir("/home/user/staging"), "/home/user/staging directory was not created."
    assert os.path.isdir("/home/user/repository"), "/home/user/repository directory was not created."

def test_benign_upload():
    """Test that a benign payload is accepted and stored correctly."""
    response = requests.post(f"{BASE_URL}/upload", data=BENIGN_PAYLOAD, timeout=5)
    assert response.status_code == 201, f"Expected 201 Created for benign payload, got {response.status_code}. Response: {response.text}"

    sha256_hash = hashlib.sha256(BENIGN_PAYLOAD).hexdigest()
    expected_file = f"/home/user/repository/{sha256_hash}.pkg"
    assert os.path.exists(expected_file), f"Expected file {expected_file} to exist in repository."

    with open(expected_file, "rb") as f:
        assert f.read() == BENIGN_PAYLOAD, "Stored file contents do not match the uploaded payload."

def test_malicious_upload():
    """Test that a malicious payload is rejected and not stored."""
    response = requests.post(f"{BASE_URL}/upload", data=MALICIOUS_PAYLOAD, timeout=5)
    assert response.status_code == 406, f"Expected 406 Not Acceptable for malicious payload, got {response.status_code}. Response: {response.text}"

    sha256_hash = hashlib.sha256(MALICIOUS_PAYLOAD).hexdigest()
    unexpected_file = f"/home/user/repository/{sha256_hash}.pkg"
    assert not os.path.exists(unexpected_file), f"Malicious file {unexpected_file} should not exist in repository."

    # Check that staging directory is empty (cleanup was performed)
    staging_dir = "/home/user/staging"
    if os.path.exists(staging_dir):
        files = os.listdir(staging_dir)
        assert len(files) == 0, f"Staging directory {staging_dir} should be empty after processing, found: {files}"

def test_audit():
    """Test that the audit endpoint returns the correct aggregated metadata."""
    response = requests.get(f"{BASE_URL}/audit", timeout=5)
    assert response.status_code == 200, f"Expected 200 OK for audit, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Audit response is not valid JSON. Response: {response.text}")

    expected_json = ["bin/startup.sh", "lib/core.so"]
    assert data == expected_json, f"Expected audit response {expected_json}, got {data}"