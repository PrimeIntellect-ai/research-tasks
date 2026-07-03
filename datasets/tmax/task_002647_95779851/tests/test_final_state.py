# test_final_state.py

import requests
import pytest

PORT = 9090
TOKEN = "TangoDown"
PAYLOAD = "Invoke-Evasion"
URL = f"http://127.0.0.1:{PORT}/download"

def test_server_responds_with_correct_payload():
    """
    Verify that the server responds with the correct payload when the proper X-Auth header is provided.
    """
    headers = {"X-Auth": TOKEN}

    try:
        response = requests.get(URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}. Ensure the server is running on port {PORT}. Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"
    assert response.text.strip() == PAYLOAD, f"Expected payload '{PAYLOAD}', got '{response.text}'"

def test_server_rejects_missing_header():
    """
    Verify that the server returns a 403 Forbidden when the X-Auth header is missing.
    """
    try:
        response = requests.get(URL, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}. Ensure the server is running on port {PORT}. Error: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 Forbidden for missing header, got {response.status_code}. Response body: {response.text}"

def test_server_rejects_incorrect_header():
    """
    Verify that the server returns a 403 Forbidden when an incorrect X-Auth header is provided.
    """
    headers = {"X-Auth": "InvalidToken123"}

    try:
        response = requests.get(URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}. Ensure the server is running on port {PORT}. Error: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 Forbidden for incorrect header, got {response.status_code}. Response body: {response.text}"