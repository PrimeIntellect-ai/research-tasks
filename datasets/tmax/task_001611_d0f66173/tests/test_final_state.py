# test_final_state.py

import os
import json
import base64
import hmac
import hashlib
import requests
import pytest
import ssl
import socket

def create_jwt(payload, secret, alg="HS256"):
    header = {"alg": alg, "typ": "JWT"}

    def b64encode(data):
        return base64.urlsafe_b64encode(data).rstrip(b'=')

    encoded_header = b64encode(json.dumps(header).encode('utf-8'))
    encoded_payload = b64encode(json.dumps(payload).encode('utf-8'))

    msg = encoded_header + b"." + encoded_payload

    if alg == "none":
        return (msg + b".").decode('utf-8')
    elif alg == "HS256":
        sig = hmac.new(secret.encode('utf-8'), msg, hashlib.sha256).digest()
        encoded_sig = b64encode(sig)
        return (msg + b"." + encoded_sig).decode('utf-8')
    else:
        raise ValueError("Unsupported algorithm")

def test_key_password_cracked():
    path = "/home/user/key_password.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "4829", f"Incorrect password in {path}. Expected '4829', got '{content}'."

def test_fullchain_exists():
    path = "/app/vendored/jwt-auth-svc-1.2.0/certs/fullchain.pem"
    assert os.path.isfile(path), f"File {path} does not exist. Did you assemble the certificate chain?"

def test_service_listening_http():
    # Check if we can connect to 8080
    try:
        r = requests.get("http://127.0.0.1:8080/api/secure", timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not listening on HTTP port 8080 or crashed.")

def test_service_listening_https_and_cert_chain():
    # Check if we can connect to 8443 and if the certificate chain is valid against root.pem
    root_pem = "/app/vendored/jwt-auth-svc-1.2.0/certs/root.pem"
    try:
        r = requests.get("https://127.0.0.1:8443/api/secure", verify=root_pem, timeout=2)
    except requests.exceptions.SSLError as e:
        pytest.fail(f"SSL/TLS Handshake failed. Certificate chain might be incorrect or not trusted by root.pem. Error: {e}")
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not listening on HTTPS port 8443 or crashed.")

def test_http_auth_missing():
    r = requests.get("http://127.0.0.1:8080/api/secure", timeout=2)
    assert r.status_code == 401, f"Expected 401 for missing auth, got {r.status_code}"

def test_http_auth_valid():
    token = create_jwt({"sub": "admin"}, "super-secret-dev-key", alg="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("http://127.0.0.1:8080/api/secure", headers=headers, timeout=2)
    assert r.status_code == 200, f"Expected 200 for valid auth, got {r.status_code}. Response: {r.text}"

def test_http_auth_forged_alg_none():
    token = create_jwt({"sub": "admin"}, "super-secret-dev-key", alg="none")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("http://127.0.0.1:8080/api/secure", headers=headers, timeout=2)
    assert r.status_code == 401, f"Expected 401 for forged alg=none token, got {r.status_code}. The vulnerability is not fixed."

def test_https_auth_valid():
    root_pem = "/app/vendored/jwt-auth-svc-1.2.0/certs/root.pem"
    token = create_jwt({"sub": "admin"}, "super-secret-dev-key", alg="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("https://127.0.0.1:8443/api/secure", headers=headers, verify=root_pem, timeout=2)
    assert r.status_code == 200, f"Expected 200 for valid auth on HTTPS, got {r.status_code}."