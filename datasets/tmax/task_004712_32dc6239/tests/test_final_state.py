# test_final_state.py

import os
import socket
import hashlib
import binascii
import subprocess
import requests
import pytest

def test_binary_exists():
    binary_path = "/home/user/ffuf_fixed"
    assert os.path.isfile(binary_path), f"The binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

def test_http_interface():
    try:
        response = requests.get("http://127.0.0.1:8080/scan", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP interface on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert "ffuf version: 2.0.0" in response.text, f"Expected 'ffuf version: 2.0.0' in response, got: {response.text}"

def get_encrypted_payload(plaintext: bytes) -> str:
    key_hex = binascii.hexlify(b"0123456789abcdef0123456789abcdef").decode()
    iv_hex = binascii.hexlify(b"abcdef0123456789").decode()

    cmd = ["openssl", "enc", "-aes-256-cbc", "-K", key_hex, "-iv", iv_hex]
    res = subprocess.run(cmd, input=plaintext, capture_output=True, check=True)
    return binascii.hexlify(res.stdout).decode()

def test_tcp_interface_valid():
    binary_path = "/home/user/ffuf_fixed"
    assert os.path.isfile(binary_path), "Cannot run TCP test: binary missing."

    with open(binary_path, "rb") as f:
        expected_hash = hashlib.sha256(f.read()).hexdigest()

    payload = get_encrypted_payload(b"VERIFY_INTEGRITY") + "\n"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(("127.0.0.1", 8081))
        s.sendall(payload.encode())
        response = s.recv(1024).decode().strip()
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to communicate with TCP interface on port 8081: {e}")

    assert response == expected_hash, f"Expected hash {expected_hash}, got {response}"

def test_tcp_interface_invalid():
    payload = "00112233445566778899aabbccddeeff\n"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(("127.0.0.1", 8081))
        s.sendall(payload.encode())
        response = s.recv(1024).decode().strip()
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to communicate with TCP interface on port 8081: {e}")

    assert response == "INVALID", f"Expected 'INVALID' for bad payload, got {response}"