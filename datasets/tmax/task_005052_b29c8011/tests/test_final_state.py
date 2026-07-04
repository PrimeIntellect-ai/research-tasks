# test_final_state.py
import os
import stat
import requests
import pytest

TOKEN_FILE = "/home/user/token.txt"
EXPECTED_TOKEN = "SECURE99"
BASE_URL = "http://127.0.0.1:8000/upload"
UPLOAD_DIR = "/home/user/uploads"

def test_token_file_exists_and_correct():
    """Verify the token was correctly decoded and saved."""
    assert os.path.exists(TOKEN_FILE), f"Token file {TOKEN_FILE} does not exist."
    with open(TOKEN_FILE, "r") as f:
        content = f.read().strip()
    assert content == EXPECTED_TOKEN, f"Expected token {EXPECTED_TOKEN}, but got {content} in {TOKEN_FILE}."

def test_missing_auth():
    """Verify that requests without an auth token are rejected with 401."""
    files = {'file': ('test.wav', b'dummy data')}
    try:
        response = requests.post(BASE_URL, files=files, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}. Response: {response.text}"

def test_invalid_auth():
    """Verify that requests with an invalid auth token are rejected with 401."""
    headers = {'X-Auth-Token': 'FAKE123'}
    files = {'file': ('test.wav', b'dummy data')}
    try:
        response = requests.post(BASE_URL, headers=headers, files=files, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for invalid auth, got {response.status_code}. Response: {response.text}"

def test_valid_request_and_permissions():
    """Verify a valid request succeeds and saves the file with 0600 permissions."""
    headers = {'X-Auth-Token': EXPECTED_TOKEN}
    files = {'file': ('legit.wav', b'dummy data')}
    data = {'filename': 'legit.wav'}

    try:
        response = requests.post(BASE_URL, headers=headers, files=files, data=data, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code in (200, 201), f"Expected HTTP 200/201 for valid request, got {response.status_code}. Response: {response.text}"

    saved_file_path = os.path.join(UPLOAD_DIR, 'legit.wav')
    assert os.path.exists(saved_file_path), f"File was not saved at {saved_file_path}."

    file_stat = os.stat(saved_file_path)
    permissions = stat.S_IMODE(file_stat.st_mode)
    assert permissions == 0o600, f"Expected file permissions 0600, got {oct(permissions)}."

def test_path_traversal_mitigation():
    """Verify that path traversal attempts are mitigated."""
    headers = {'X-Auth-Token': EXPECTED_TOKEN}
    files = {'file': ('hacked.wav', b'dummy data')}
    data = {'filename': '../../hacked.wav'}

    try:
        response = requests.post(BASE_URL, headers=headers, files=files, data=data, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code in (200, 201, 400), f"Expected HTTP 200, 201, or 400 for traversal attempt, got {response.status_code}. Response: {response.text}"

    traversal_target = "/home/user/hacked.wav"
    assert not os.path.exists(traversal_target), f"Path traversal vulnerability exists! File was saved to {traversal_target}."

    if response.status_code in (200, 201):
        sanitized_target = os.path.join(UPLOAD_DIR, 'hacked.wav')
        assert os.path.exists(sanitized_target), f"Expected sanitized file to be saved at {sanitized_target}, but it was not found."