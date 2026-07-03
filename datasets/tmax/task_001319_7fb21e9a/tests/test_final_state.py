# test_final_state.py

import os
import stat
import socket
import pytest
import requests
import urllib3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Disable insecure request warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

APP_DIR = "/home/user/app"
NGINX_URL = "https://127.0.0.1:8443/auth"
BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 8081

def test_ssh_key_permissions():
    id_rsa_path = os.path.join(APP_DIR, ".ssh", "id_rsa")
    assert os.path.isfile(id_rsa_path), f"SSH private key {id_rsa_path} does not exist."

    st = os.stat(id_rsa_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o600, f"Expected {id_rsa_path} to have 0600 permissions, got {oct(permissions)}."

def test_nginx_rejects_without_header():
    try:
        response = requests.get(NGINX_URL, verify=False, timeout=5)
        assert response.status_code in [400, 403], f"Expected Nginx to reject request without header with 400 or 403, got {response.status_code}."
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to Nginx on port 8443. Is it running?")

def test_nginx_accepts_with_header():
    headers = {"X-Auditor-Auth": "true"}
    try:
        response = requests.get(NGINX_URL, headers=headers, verify=False, timeout=5)
        # We expect the request to be forwarded to the backend. 
        # The backend might return a specific response or close the connection if it expects raw TCP AES data, 
        # but at minimum Nginx should not block it with 400/403.
        assert response.status_code not in [400, 403], f"Nginx rejected valid request with {response.status_code}."
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to Nginx on port 8443.")

def test_backend_aes_decryption():
    key = b"0123456789abcdef"
    iv = b"abcdef9876543210"
    plaintext_token = b"test_token_12345"

    # Pad the plaintext to 16 bytes (AES block size)
    pad_len = 16 - (len(plaintext_token) % 16)
    padded_token = plaintext_token + bytes([pad_len] * pad_len)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_token) + encryptor.finalize()

    try:
        with socket.create_connection((BACKEND_HOST, BACKEND_PORT), timeout=5) as s:
            s.sendall(ciphertext)
            response = s.recv(1024).decode('utf-8', errors='ignore')

            assert "Set-Cookie: session=" in response, "Backend did not return the expected Set-Cookie header."
            assert "Secure" in response and "HttpOnly" in response, "Cookie is missing Secure or HttpOnly flags."

    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to backend at {BACKEND_HOST}:{BACKEND_PORT}.")
    except socket.timeout:
        pytest.fail("Backend connection timed out.")

def test_backend_source_code():
    backend_path = os.path.join(APP_DIR, "backend.c")
    assert os.path.isfile(backend_path), f"File {backend_path} does not exist."

    with open(backend_path, 'r') as f:
        content = f.read()

    assert "<openssl/aes.h>" in content or "<openssl/evp.h>" in content, "Backend source does not seem to include OpenSSL headers."