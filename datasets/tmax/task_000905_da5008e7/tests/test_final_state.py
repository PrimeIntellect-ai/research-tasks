# test_final_state.py

import os
import json
import stat
import pytest
import requests

def test_bug_fixed_in_server_py():
    path = "/app/auth_proxy-1.2.3/auth_proxy/server.py"
    assert os.path.isfile(path), f"server.py is missing: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "Authorisation" not in content, "The typo 'Authorisation' was not fixed in server.py"
    assert "Authorization" in content, "The correct header 'Authorization' is missing in server.py"

def test_deploy_script_exists_and_executable():
    path = "/home/user/deploy.sh"
    assert os.path.isfile(path), f"Deployment script missing: {path}"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deployment script is not executable: {path}"

def test_check_health_script_exists_and_executable():
    path = "/home/user/check_health.sh"
    assert os.path.isfile(path), f"Health check script missing: {path}"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Health check script is not executable: {path}"

def test_users_json_exists_and_correct():
    path = "/home/user/users.json"
    assert os.path.isfile(path), f"users.json missing: {path}"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {path}")

    expected_users = [
        {"username": "admin", "token": "super-secret-99", "group": "sysadmin"},
        {"username": "guest", "token": "guest-token-11", "group": "readonly"}
    ]

    assert "users" in data, "Key 'users' missing in users.json"

    # Check if expected users are present
    for expected_user in expected_users:
        assert expected_user in data["users"], f"Expected user {expected_user} not found in users.json"

def test_venv_exists():
    path = "/home/user/venv"
    assert os.path.isdir(path), f"Virtual environment directory missing: {path}"
    python_bin = os.path.join(path, "bin", "python")
    assert os.path.isfile(python_bin), f"Python binary missing in venv: {python_bin}"

def test_service_running_and_responds_correctly():
    url = "http://127.0.0.1:9090/api/whoami"

    # Test valid token
    headers = {"Authorization": "Bearer super-secret-99"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail("Service did not return valid JSON")

    assert data.get("username") == "admin", "Expected username 'admin'"
    assert data.get("group") == "sysadmin", "Expected group 'sysadmin'"

def test_service_unauthorized_response():
    url = "http://127.0.0.1:9090/api/whoami"

    # Test invalid token
    headers = {"Authorization": "Bearer invalid-token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for invalid token, got {response.status_code}"

    # Test missing auth header
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for missing auth header, got {response.status_code}"