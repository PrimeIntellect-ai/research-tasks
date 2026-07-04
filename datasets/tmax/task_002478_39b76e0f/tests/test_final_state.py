# test_final_state.py

import os
import requests
import pytest

def test_setup_py_fixed():
    setup_path = "/app/file_vault/setup.py"
    assert os.path.isfile(setup_path), f"File {setup_path} is missing."
    with open(setup_path, "r") as f:
        content = f.read()
    assert "flask" in content.lower(), f"The dependency 'flask' is missing in {setup_path}. Did you fix the typo?"
    assert "flsk" not in content.lower(), f"The typo 'flsk' is still present in {setup_path}."

def test_recovered_token_file():
    token_path = "/home/user/evidence/recovered_token.txt"
    assert os.path.isfile(token_path), f"File {token_path} is missing."
    with open(token_path, "r") as f:
        content = f.read().strip()
    assert content == "s3cr3t_admin_t0k3n", f"The recovered token in {token_path} is incorrect."

def test_service_valid_upload():
    url = "http://127.0.0.1:9090/upload"
    headers = {"Authorization": "Bearer s3cr3t_admin_t0k3n"}
    files = {"file": ("test.txt", b"dummy content")}
    try:
        response = requests.post(url, headers=headers, files=files, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for valid upload, got {response.status_code}. Response: {response.text}"

def test_service_invalid_auth():
    url = "http://127.0.0.1:9090/upload"
    headers = {"Authorization": "Bearer wrongtoken"}
    files = {"file": ("test.txt", b"dummy content")}
    try:
        response = requests.post(url, headers=headers, files=files, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for invalid auth, got {response.status_code}. Response: {response.text}"

def test_service_path_traversal_blocked():
    url = "http://127.0.0.1:9090/upload"
    headers = {"Authorization": "Bearer s3cr3t_admin_t0k3n"}
    files = {"file": ("../../../etc/passwd", b"dummy content")}
    try:
        response = requests.post(url, headers=headers, files=files, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code in (400, 403), f"Expected HTTP 400 or 403 for path traversal attempt, got {response.status_code}. Response: {response.text}"