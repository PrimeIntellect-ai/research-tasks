# test_final_state.py

import os
import stat
import requests
import pytest

PAYLOAD_PATH = "/app/payload.bin"
EXPECTED_PAYLOAD_CONTENT = "EVASION_STAGE_2_READY"
SERVER_URL = "http://127.0.0.1:8080/payload"
EXPECTED_TOKEN = "6c5ea1f29ba04a58b273b5dfbe74f1b52a1eb2974e11244ab9bce413c2c77d54"

def test_payload_file_exists_and_content():
    """Verify that the payload file exists and contains the correct text."""
    assert os.path.exists(PAYLOAD_PATH), f"File {PAYLOAD_PATH} does not exist."
    assert os.path.isfile(PAYLOAD_PATH), f"{PAYLOAD_PATH} is not a regular file."

    with open(PAYLOAD_PATH, "r") as f:
        content = f.read().strip()

    assert content == EXPECTED_PAYLOAD_CONTENT, f"Payload content is incorrect. Expected '{EXPECTED_PAYLOAD_CONTENT}', got '{content}'."

def test_payload_file_permissions():
    """Verify that the payload file has strictly 0400 permissions."""
    assert os.path.exists(PAYLOAD_PATH), f"File {PAYLOAD_PATH} does not exist."

    st = os.stat(PAYLOAD_PATH)
    perms = stat.S_IMODE(st.st_mode)

    # 0400 in octal is 256 in decimal
    assert perms == 0o400, f"Payload file permissions are incorrect. Expected 0400, got {oct(perms)}."

def test_server_authenticated_request():
    """Verify that the server responds correctly to an authenticated request."""
    headers = {"X-Evasion-Token": EXPECTED_TOKEN}
    try:
        response = requests.get(SERVER_URL, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the server at {SERVER_URL}. Is it running?")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {SERVER_URL} timed out.")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}."
    assert response.text.strip() == EXPECTED_PAYLOAD_CONTENT, f"Expected response body '{EXPECTED_PAYLOAD_CONTENT}', got '{response.text}'."

def test_server_unauthenticated_request_missing_header():
    """Verify that the server rejects requests without the token header."""
    try:
        response = requests.get(SERVER_URL, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the server at {SERVER_URL}. Is it running?")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {SERVER_URL} timed out.")

    assert response.status_code == 403, f"Expected HTTP 403 Forbidden for missing header, got {response.status_code}."

def test_server_unauthenticated_request_wrong_header():
    """Verify that the server rejects requests with an incorrect token."""
    headers = {"X-Evasion-Token": "invalid_token_12345"}
    try:
        response = requests.get(SERVER_URL, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the server at {SERVER_URL}. Is it running?")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {SERVER_URL} timed out.")

    assert response.status_code == 403, f"Expected HTTP 403 Forbidden for incorrect token, got {response.status_code}."