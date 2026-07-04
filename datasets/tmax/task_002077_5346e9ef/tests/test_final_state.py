# test_final_state.py

import os
import requests
import pytest
import time

def test_decrypted_evidence():
    decrypted_path = "/app/evidence/decrypted.txt"
    assert os.path.isfile(decrypted_path), f"Decrypted evidence file not found at {decrypted_path}"

    with open(decrypted_path, "r") as f:
        content = f.read().strip()

    expected_token = "AUTH_TOKEN: 8f9b2a1c-7e6d-4f5a-9b2c-1d9e8f7a6b5c"
    assert content == expected_token, f"Decrypted text does not match the expected token. Got: {content}"

def test_server_token_endpoint():
    url = "http://localhost:8080/token"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go server at {url}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 from /token, got {response.status_code}"

    expected_token = "AUTH_TOKEN: 8f9b2a1c-7e6d-4f5a-9b2c-1d9e8f7a6b5c"
    assert response.text.strip() == expected_token, f"Expected response body to be '{expected_token}', got '{response.text}'"

def test_server_upload_path_traversal_mitigation():
    url = "http://localhost:8080/upload"

    # Ensure the target malicious path does not exist before the test
    evil_file_path = "/tmp/evil.txt"
    if os.path.exists(evil_file_path):
        os.remove(evil_file_path)

    files = {
        'file': ('../../../tmp/evil.txt', b'malicious content')
    }

    try:
        response = requests.post(url, files=files, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go server at {url}. Error: {e}")

    # The server should either reject it (4xx/5xx) or sanitize it.
    # The primary check is that the path traversal failed.
    assert not os.path.exists(evil_file_path), "Path traversal vulnerability still exists! File was written to /tmp/evil.txt"

    # If it was sanitized, it should be in /app/server/uploads/evil.txt or similar, 
    # but the main requirement is that it did NOT write to /tmp/evil.txt.