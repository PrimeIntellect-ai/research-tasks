# test_final_state.py

import os
import requests
import pytest
import socket

SECRET = "zk9_f83jf92_git_leak_99"
AUTH_HEADER = {"Authorization": f"Bearer {SECRET}"}
BASE_URL = "http://127.0.0.1:8080/api/v1/auth"

def test_env_file_exists_and_contains_secret():
    """Check that the .env file exists and contains the correct secret."""
    env_path = "/app/auth-service/.env"
    assert os.path.isfile(env_path), f"{env_path} is missing."
    with open(env_path, "r") as f:
        content = f.read()
    assert f"SECRET_API_KEY={SECRET}" in content, "The .env file does not contain the correct SECRET_API_KEY."

def test_redis_running():
    """Check that Redis is listening on port 6380."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex(('127.0.0.1', 6380))
        assert result == 0, "Redis server is not listening on 127.0.0.1:6380."

def test_rust_service_running():
    """Check that the Rust service is listening on port 8080."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex(('127.0.0.1', 8080))
        assert result == 0, "Rust service is not listening on 127.0.0.1:8080."

def test_valid_payload():
    """Test that a valid payload returns 200 OK."""
    try:
        response = requests.post(
            BASE_URL,
            json={"client_id": "client_1", "payload": "SGVsbG8="},
            headers=AUTH_HEADER,
            timeout=5
        )
    except requests.RequestException as e:
        pytest.fail(f"Request failed: {e}")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

def test_missing_client_id():
    """Test that missing client_id returns 400 Bad Request."""
    try:
        response = requests.post(
            BASE_URL,
            json={"payload": "SGVsbG8="},
            headers=AUTH_HEADER,
            timeout=5
        )
    except requests.RequestException as e:
        pytest.fail(f"Request failed: {e}")
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}. Response: {response.text}"

def test_unpadded_base64():
    """Test that unpadded Base64 returns 200 OK."""
    try:
        response = requests.post(
            BASE_URL,
            json={"client_id": "client_2", "payload": "SGVsbG8"},
            headers=AUTH_HEADER,
            timeout=5
        )
    except requests.RequestException as e:
        pytest.fail(f"Request failed: {e}")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

def test_invalid_utf8_base64():
    """Test that invalid UTF-8 Base64 returns 200 OK."""
    try:
        response = requests.post(
            BASE_URL,
            json={"client_id": "client_3", "payload": "//5I"},
            headers=AUTH_HEADER,
            timeout=5
        )
    except requests.RequestException as e:
        pytest.fail(f"Request failed: {e}")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"