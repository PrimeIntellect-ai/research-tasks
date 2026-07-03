# test_final_state.py
import requests
import pytest
import base64

URL = "http://127.0.0.1:8000/validate"
TOKEN = "SEC-TKN-88A21F9C"

def test_missing_token_returns_401():
    """Send POST /validate with no headers. Expect: 401 Unauthorized."""
    try:
        response = requests.post(URL, json={"command": "ZWNobywiaGVsbG8i"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for missing token, but got {response.status_code}. Response: {response.text}"

def test_valid_token_benign_command_returns_200():
    """Send POST /validate with valid token and benign command. Expect: 200 OK."""
    headers = {"X-Policy-Token": TOKEN}
    # base64 for 'echo "hello"'
    payload = {"command": "ZWNobywiaGVsbG8i"}

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200 for valid token and benign command, but got {response.status_code}. Response: {response.text}"

def test_valid_token_malicious_command_returns_403():
    """Send POST /validate with valid token and malicious command matching regex. Expect: 403 Forbidden."""
    headers = {"X-Policy-Token": TOKEN}
    # base64 for 'shellcode e9 9090A1B2 here'
    payload = {"command": "c2hlbGxjb2RlIGU5IDkwOTBBMUIyIGhlcmU="}

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 403, f"Expected status code 403 for valid token and malicious command, but got {response.status_code}. Response: {response.text}"

def test_valid_token_malicious_command_with_0x_returns_403():
    """Send POST /validate with valid token and another malicious command matching regex. Expect: 403 Forbidden."""
    headers = {"X-Policy-Token": TOKEN}
    # base64 for 'bad 0xE9 12345678 inject'
    payload = {"command": "YmFkIDB4RTkgMTIzNDU2NzggaW5qZWN0"}

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 403, f"Expected status code 403 for valid token and malicious command with 0x prefix, but got {response.status_code}. Response: {response.text}"