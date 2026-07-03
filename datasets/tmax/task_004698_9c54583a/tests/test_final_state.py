# test_final_state.py
import os
import stat
import json
import subprocess
import requests

def test_config_file_permissions():
    config_path = "/home/user/capacity_config.json"
    assert os.path.exists(config_path), f"Config file {config_path} does not exist."

    st = os.stat(config_path)
    perms = stat.S_IMODE(st.st_mode)

    # Check that group and others have no permissions
    assert (perms & stat.S_IRWXG) == 0, f"Group has permissions on {config_path}: {oct(perms)}"
    assert (perms & stat.S_IRWXO) == 0, f"Others have permissions on {config_path}: {oct(perms)}"

    # Check that owner has read permission
    assert (perms & stat.S_IRUSR) != 0, f"Owner does not have read permission on {config_path}"

def test_systemd_service_exists():
    service_file = "/home/user/.config/systemd/user/capacity-planner.service"
    assert os.path.exists(service_file), f"Systemd user service file {service_file} is missing."

def test_api_response():
    url = "http://127.0.0.1:8123/api/v1/capacity"
    headers = {"X-Planner-Auth": "700700"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the API at {url}: {e}"

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {response.text}"

    expected_data = {
        "cpu_threshold": 85,
        "source": "init_db",
        "status": "analyzing"
    }

    assert data == expected_data, f"Unexpected JSON response. Expected {expected_data}, got {data}"

def test_api_auth_failure():
    url = "http://127.0.0.1:8123/api/v1/capacity"
    headers = {"X-Planner-Auth": "wrongpin"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the API at {url}: {e}"

    assert response.status_code != 200, "API did not reject invalid authentication"