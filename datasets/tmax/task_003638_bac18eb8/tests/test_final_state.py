# test_final_state.py
import os
import zlib
import json
import pytest
import requests

TOKEN = "8A4F-99B2-C7E1-XYZ9"
NGINX_URL = "http://127.0.0.1:8000/upload"
C_SERVER_URL = "http://127.0.0.1:8080/upload"

def test_nginx_rejects_non_post():
    """Test that Nginx rejects GET requests with 405 Method Not Allowed."""
    try:
        response = requests.get(NGINX_URL, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {NGINX_URL}: {e}")

    assert response.status_code == 405, f"Expected HTTP 405 for GET request, got {response.status_code}"

def test_unauthorized_post_rejected():
    """Test that POST requests without the correct Auth header are rejected with 401."""
    try:
        response = requests.post(NGINX_URL, data=b"HelloWorld", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {NGINX_URL}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing Auth header, got {response.status_code}"

def test_successful_post_crc32():
    """Test that a valid POST request returns 200 and the correct CRC32 checksum."""
    payload = b"HelloWorld"
    expected_crc32 = f"{zlib.crc32(payload) & 0xFFFFFFFF:08x}"
    headers = {"Authorization": f"Bearer {TOKEN}"}

    try:
        response = requests.post(NGINX_URL, data=payload, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {NGINX_URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for valid request, got {response.status_code}. Response: {response.text}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type: application/json"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("checksum") == expected_crc32, f"Expected checksum '{expected_crc32}', got {data.get('checksum')}"

def test_c_server_directly():
    """Test the C server directly to ensure it is running on port 8080."""
    payload = b"DirectTest"
    expected_crc32 = f"{zlib.crc32(payload) & 0xFFFFFFFF:08x}"
    headers = {"Authorization": f"Bearer {TOKEN}"}

    try:
        response = requests.post(C_SERVER_URL, data=payload, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to C server at {C_SERVER_URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 from C server, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"C server response body is not valid JSON: {response.text}")

    assert data.get("checksum") == expected_crc32, f"Expected checksum '{expected_crc32}' from C server, got {data.get('checksum')}"

def test_upload_script_exists_and_executable():
    """Test that the upload script exists, is executable, and contains the required elements."""
    script_path = "/home/user/upload_artifact.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist"
    assert os.path.isfile(script_path), f"{script_path} is not a file"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

    with open(script_path, "r") as f:
        content = f.read()

    assert "curl" in content, "Script does not use curl"
    assert "127.0.0.1:8000/upload" in content or "localhost:8000/upload" in content, "Script does not point to the correct Nginx URL"
    assert TOKEN in content, "Script does not contain the extracted token"