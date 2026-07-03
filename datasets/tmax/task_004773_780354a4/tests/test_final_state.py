# test_final_state.py

import os
import struct
import requests
import pytest
import time

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}/upload"
AUTH_HEADER = {"Authorization": "Bearer golden eagle"}
EXTRACT_DIR = "/home/user/artifacts"

def create_artf_payload(files):
    """
    files is a list of tuples: (filename: str, content: bytes)
    """
    payload = b"ARTF"
    payload += struct.pack("<H", len(files))
    for filename, content in files:
        filename_bytes = filename.encode('ascii')
        payload += struct.pack("<H", len(filename_bytes))
        payload += filename_bytes
        payload += struct.pack("<I", len(content))
        payload += content
    return payload

def wait_for_server():
    """Wait briefly for the server to be ready."""
    for _ in range(10):
        try:
            requests.get(f"http://127.0.0.1:{PORT}/", timeout=0.5)
            return
        except requests.exceptions.RequestException:
            time.sleep(0.5)

@pytest.fixture(scope="module", autouse=True)
def setup():
    wait_for_server()

def test_missing_auth():
    payload = create_artf_payload([("dummy.txt", b"dummy")])
    try:
        response = requests.post(BASE_URL, data=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth, got {response.status_code}"

def test_valid_archive_extraction():
    payload = create_artf_payload([("test.txt", b"hello")])
    try:
        response = requests.post(BASE_URL, headers=AUTH_HEADER, data=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert response.status_code == 200, f"Expected 200 OK for valid archive, got {response.status_code}"

    extracted_file_path = os.path.join(EXTRACT_DIR, "test.txt")
    assert os.path.isfile(extracted_file_path), f"Expected extracted file at {extracted_file_path} does not exist"

    with open(extracted_file_path, "rb") as f:
        content = f.read()
    assert content == b"hello", f"Expected extracted file content to be 'hello', got {content}"

def test_malicious_archive_rejection():
    payload = create_artf_payload([("../hacked.txt", b"bad")])
    try:
        response = requests.post(BASE_URL, headers=AUTH_HEADER, data=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert response.status_code == 400, f"Expected 400 Bad Request for malicious archive, got {response.status_code}"

    hacked_file_path_1 = "/home/user/hacked.txt"
    hacked_file_path_2 = os.path.normpath(os.path.join(EXTRACT_DIR, "../hacked.txt"))

    assert not os.path.exists(hacked_file_path_1), f"Malicious file was extracted to {hacked_file_path_1}"
    assert not os.path.exists(hacked_file_path_2), f"Malicious file was extracted to {hacked_file_path_2}"