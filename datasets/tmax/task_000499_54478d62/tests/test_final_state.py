# test_final_state.py

import os
import socket
import requests
import pytest

def test_nginx_routing():
    """Verify Nginx is listening on 8080 and routing to the Flask app."""
    try:
        response = requests.get("http://127.0.0.1:8080/", timeout=2)
        assert response.status_code == 200, f"Expected HTTP 200 from Nginx routing to Flask, got {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")

def test_exploit_payload_success():
    """Verify the exploit payload triggers the ADMIN_GRANTED state in the auth daemon."""
    payload_path = "/home/user/exploit_payload.txt"
    assert os.path.isfile(payload_path), f"Exploit payload file missing at {payload_path}"

    with open(payload_path, "rb") as f:
        payload = f.read()

    try:
        with socket.create_connection(("127.0.0.1", 9000), timeout=2) as sock:
            sock.sendall(payload)
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            assert "ADMIN_GRANTED" in response, f"Payload did not trigger ADMIN_GRANTED. Daemon responded with: {response}"
    except ConnectionRefusedError:
        pytest.fail("Could not connect to auth-daemon on 127.0.0.1:9000. Is it running?")
    except socket.timeout:
        pytest.fail("Connection to auth-daemon timed out.")

def test_patch_valid_username():
    """Verify the patched Flask app accepts valid usernames."""
    try:
        response = requests.post("http://127.0.0.1:8080/check_access", data={"username": "admin"}, timeout=2)
        assert response.status_code == 200, f"Expected HTTP 200 for valid username 'admin', got {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Flask app via Nginx: {e}")

def test_patch_adversarial_length():
    """Verify the patched Flask app rejects usernames exceeding 16 characters."""
    long_username = "A" * 20
    try:
        response = requests.post("http://127.0.0.1:8080/check_access", data={"username": long_username}, timeout=2)
        assert response.status_code == 400, f"Expected HTTP 400 for overly long username, got {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Flask app via Nginx: {e}")

def test_patch_adversarial_characters():
    """Verify the patched Flask app rejects non-alphanumeric usernames."""
    bad_username = "admin;drop"
    try:
        response = requests.post("http://127.0.0.1:8080/check_access", data={"username": bad_username}, timeout=2)
        assert response.status_code == 400, f"Expected HTTP 400 for non-alphanumeric username, got {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Flask app via Nginx: {e}")