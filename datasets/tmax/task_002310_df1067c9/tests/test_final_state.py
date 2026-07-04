# test_final_state.py
import os
import requests
import pytest

WORKSPACE_DIR = "/home/user/workspace"
NGINX_URL = "http://127.0.0.1:8080/api/diff"
BACKEND_URL = "http://127.0.0.1:9090/internal/diff"
AUTH_TOKEN = "super-secret-token"

def test_files_exist():
    assert os.path.exists(os.path.join(WORKSPACE_DIR, "libdiffplugin.so")), "libdiffplugin.so is missing."
    assert os.path.exists(os.path.join(WORKSPACE_DIR, "nginx.conf")), "nginx.conf is missing."

def test_nginx_auth_failure():
    # Flow 1: No auth
    try:
        response = requests.post(NGINX_URL, json={"a": "1,2", "b": "2,3"}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {NGINX_URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

    # Flow 1: Wrong auth
    headers = {"Authorization": "Bearer wrong-token"}
    try:
        response = requests.post(NGINX_URL, json={"a": "1,2", "b": "2,3"}, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {NGINX_URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for wrong token, got {response.status_code}"

def test_backend_direct():
    # Flow 2: Backend Direct
    payload = {"a": "10,20,30", "b": "20,40"}
    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to backend at {BACKEND_URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK from backend, got {response.status_code}. Body: {response.text}"
    assert response.text.strip() == "10,30,40", f"Expected diff '10,30,40', got '{response.text.strip()}'"

def test_nginx_end_to_end_success():
    # Flow 3: End-to-End Success
    payload = {"a": "7,3,1,5", "b": "5,8,1,2"}
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    try:
        response = requests.post(NGINX_URL, json=payload, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {NGINX_URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK from Nginx, got {response.status_code}. Body: {response.text}"
    assert response.text.strip() == "2,3,7,8", f"Expected diff '2,3,7,8', got '{response.text.strip()}'"