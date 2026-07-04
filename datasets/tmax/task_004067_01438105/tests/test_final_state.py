# test_final_state.py

import base64
import hashlib
import requests
import pytest

KEY = b"s3cr3tK3y1234567"
URL = "http://127.0.0.1:9000/execute"

def encrypt_payload(plaintext: bytes) -> str:
    xored = bytes([b ^ KEY[i % len(KEY)] for i, b in enumerate(plaintext)])
    return base64.b64encode(xored).decode('utf-8')

def get_checksum(plaintext: bytes) -> str:
    return hashlib.sha256(plaintext).hexdigest()

def test_service_running_and_executes_command():
    command = b"echo 'hello world'"
    payload = encrypt_payload(command)
    checksum = get_checksum(command)

    try:
        response = requests.post(URL, json={"payload": payload, "checksum": checksum}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    assert "hello world" in response.text, f"Expected 'hello world' in stdout, got: {response.text}"

def test_service_invalid_checksum():
    command = b"echo 'should not run'"
    payload = encrypt_payload(command)
    checksum = "invalidchecksum1234567890abcdef"

    try:
        response = requests.post(URL, json={"payload": payload, "checksum": checksum}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {URL}: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 Forbidden for invalid checksum, got {response.status_code}"

def test_service_runs_in_sandbox_directory():
    command = b"pwd"
    payload = encrypt_payload(command)
    checksum = get_checksum(command)

    try:
        response = requests.post(URL, json={"payload": payload, "checksum": checksum}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    assert "/tmp/sandbox" in response.text, f"Expected execution in /tmp/sandbox, got: {response.text}"