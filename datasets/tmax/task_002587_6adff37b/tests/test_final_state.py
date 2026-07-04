# test_final_state.py

import os
import stat
import socket
import requests
import pytest

def test_ssh_directory_permissions():
    """Verify that the .ssh directory exists and has 700 permissions."""
    path = "/home/user/.ssh"
    assert os.path.isdir(path), f"Directory {path} does not exist."
    mode = os.stat(path).st_mode
    assert stat.S_IMODE(mode) == 0o700, f"Permissions on {path} should be 700, got {oct(stat.S_IMODE(mode))}"

def test_ssh_private_key_permissions():
    """Verify that the private key exists and has 600 permissions."""
    path = "/home/user/.ssh/id_ed25519"
    assert os.path.isfile(path), f"Private key {path} does not exist."
    mode = os.stat(path).st_mode
    assert stat.S_IMODE(mode) == 0o600, f"Permissions on {path} should be 600, got {oct(stat.S_IMODE(mode))}"

def test_http_pubkey_service():
    """Verify that the HTTP service on port 8000 serves the exact public key."""
    pubkey_path = "/home/user/.ssh/id_ed25519.pub"
    assert os.path.isfile(pubkey_path), f"Public key {pubkey_path} does not exist."

    with open(pubkey_path, "r") as f:
        expected_pubkey = f.read()

    try:
        response = requests.get("http://127.0.0.1:8000/pubkey", timeout=3)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
        assert response.text == expected_pubkey, "HTTP response body does not match the public key file contents exactly."
    except requests.RequestException as e:
        pytest.fail(f"HTTP request to port 8000 failed: {e}")

def test_tcp_auth_service_correct_pin():
    """Verify that the TCP service on port 9000 returns the decrypted payload for the correct PIN."""
    try:
        with socket.create_connection(("127.0.0.1", 9000), timeout=3) as s:
            s.sendall(b"842601\n")
            response = s.recv(4096)
            expected_payload = b"CONFIDENTIAL: OPERATION_RED_DAWN_TARGET_ACQUIRED"
            assert expected_payload in response, f"Expected decrypted payload {expected_payload!r} in response, got: {response!r}"
    except Exception as e:
        pytest.fail(f"TCP connection to port 9000 (correct PIN) failed or timed out: {e}")

def test_tcp_auth_service_incorrect_pin():
    """Verify that the TCP service on port 9000 returns ACCESS DENIED for an incorrect PIN."""
    try:
        with socket.create_connection(("127.0.0.1", 9000), timeout=3) as s:
            s.sendall(b"000000\n")
            response = s.recv(4096)
            assert b"DENIED" in response.upper(), f"Expected 'ACCESS DENIED' in response, got: {response!r}"
    except Exception as e:
        pytest.fail(f"TCP connection to port 9000 (incorrect PIN) failed or timed out: {e}")