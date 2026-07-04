# test_final_state.py
import os
import hashlib
import requests
import pytest
import urllib3

# Disable warnings for unverified HTTPS requests (self-signed certs)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_secret_data_extracted_and_verified():
    secret_path = "/home/user/secret_data.txt"
    hash_path = "/home/user/hash.txt"

    assert os.path.exists(secret_path), f"File not found: {secret_path}. Did you extract it from the archive?"
    assert os.path.exists(hash_path), f"File not found: {hash_path}."

    with open(secret_path, 'rb') as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    with open(hash_path, 'r') as f:
        expected_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Hash of {secret_path} does not match the expected hash in {hash_path}."

def test_https_server_valid_jwt_bypass():
    url = "https://127.0.0.1:8443/"
    # Header: {"alg":"none"}, Payload: {"role":"admin"}
    token = "eyJhbGciOiJub25lIn0.eyJyb2xlIjoiYWRtaW4ifQ."
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTPS server at {url}. Is socat running and bound correctly? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for a valid 'alg: none' JWT with admin role, but got {response.status_code}."

    with open("/home/user/secret_data.txt", 'r') as f:
        expected_data = f.read().strip()

    assert expected_data in response.text, "The server response did not contain the contents of secret_data.txt."

def test_https_server_invalid_role_jwt():
    url = "https://127.0.0.1:8443/"
    # Header: {"alg":"none"}, Payload: {"role":"user"}
    token = "eyJhbGciOiJub25lIn0.eyJyb2xlIjoidXNlciJ9."
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTPS server at {url}. Error: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for a JWT with a non-admin role, but got {response.status_code}."

def test_https_server_missing_jwt():
    url = "https://127.0.0.1:8443/"

    try:
        response = requests.get(url, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTPS server at {url}. Error: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized when no Authorization header is provided, but got {response.status_code}."