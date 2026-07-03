# test_final_state.py

import os
import requests
import pytest
import time

BASE_URL = "http://127.0.0.1:8080"
TOKEN = "Echo404"
ARCHIVE_PATH = "/home/user/archive.bin"

def wait_for_server():
    """Wait for the server to be up and running."""
    for _ in range(10):
        try:
            requests.get(BASE_URL)
            return
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)

@pytest.fixture(scope="session", autouse=True)
def setup_server():
    wait_for_server()

def test_upload_success_and_archive_content():
    headers = {"X-Backup-Token": TOKEN}
    payload = "ABBCCCDDDDEEEEE"

    # 1. POST /upload
    try:
        response = requests.post(f"{BASE_URL}/upload", headers=headers, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/upload: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    # 2. Inspect /home/user/archive.bin
    assert os.path.isfile(ARCHIVE_PATH), f"Archive file {ARCHIVE_PATH} was not created."

    with open(ARCHIVE_PATH, "rb") as f:
        content = f.read()

    expected_bytes = b'A\x01B\x02C\x03D\x04E\x05'
    assert content == expected_bytes, f"Archive content mismatch. Expected {expected_bytes}, got {content}"

def test_download_success():
    headers = {"X-Backup-Token": TOKEN}

    # 3. GET /download
    try:
        response = requests.get(f"{BASE_URL}/download", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/download: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert response.text == "ABBCCCDDDDEEEEE", f"Expected response body 'ABBCCCDDDDEEEEE', got '{response.text}'"

def test_invalid_token():
    headers = {"X-Backup-Token": "Invalid"}
    payload = "TEST"

    # 4. POST /upload with invalid token
    try:
        response = requests.post(f"{BASE_URL}/upload", headers=headers, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/upload: {e}")

    assert response.status_code != 200, f"Expected non-200 status for invalid token, got {response.status_code}"