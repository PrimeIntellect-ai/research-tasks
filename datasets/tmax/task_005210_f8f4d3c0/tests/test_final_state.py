# test_final_state.py

import os
import hashlib
import time
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080/cgi-bin/upload.sh"
AUTH_HEADER = "X-Audit-Auth"
AUTH_TOKEN = "reddragon_salty_42"

def wait_for_server():
    for _ in range(10):
        try:
            requests.options(BASE_URL, timeout=1)
            return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    return False

@pytest.fixture(scope="module", autouse=True)
def setup():
    assert wait_for_server(), "Server is not running on port 8080 or /cgi-bin/upload.sh is not accessible"

def test_missing_auth():
    response = requests.post(BASE_URL, data="test")
    assert response.status_code == 401, f"Expected 401 for missing auth, got {response.status_code}"

def test_incorrect_auth():
    headers = {AUTH_HEADER: "wrong_token"}
    response = requests.post(BASE_URL, headers=headers, data="test")
    assert response.status_code == 401, f"Expected 401 for incorrect auth, got {response.status_code}"

def test_path_traversal():
    headers = {
        AUTH_HEADER: AUTH_TOKEN,
        "X-Filename": "../../../tmp/hack.txt",
        "X-File-Hash": "dummy"
    }
    response = requests.post(BASE_URL, headers=headers, data="test")
    assert response.status_code == 400, f"Expected 400 for path traversal, got {response.status_code}"

def test_invalid_hash():
    headers = {
        AUTH_HEADER: AUTH_TOKEN,
        "X-Filename": "test1.txt",
        "X-File-Hash": "invalidhash"
    }
    response = requests.post(BASE_URL, headers=headers, data="audit payload")
    assert response.status_code == 422, f"Expected 422 for invalid hash, got {response.status_code}"
    assert not os.path.exists("/app/audit_logs/test1.txt"), "File should not be saved if hash is invalid"

def test_successful_upload():
    payload = b"audit payload"
    payload_hash = hashlib.sha256(payload).hexdigest()
    filename = "test_success.txt"
    headers = {
        AUTH_HEADER: AUTH_TOKEN,
        "X-Filename": filename,
        "X-File-Hash": payload_hash
    }
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 200, f"Expected 200 for successful upload, got {response.status_code}"
    assert "SUCCESS" in response.text, f"Expected 'SUCCESS' in response body, got {response.text}"

    file_path = f"/app/audit_logs/{filename}"
    assert os.path.exists(file_path), f"File {file_path} was not saved"
    with open(file_path, "rb") as f:
        assert f.read() == payload, "Saved file content does not match payload"