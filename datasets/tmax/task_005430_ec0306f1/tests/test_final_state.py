# test_final_state.py

import os
import requests
import pytest
import time

def test_files_exist():
    app_dir = "/home/user/app"
    assert os.path.isfile(os.path.join(app_dir, "nginx.conf")), "nginx.conf is missing"
    assert os.path.isfile(os.path.join(app_dir, "router.py")), "router.py is missing"
    assert os.path.isfile(os.path.join(app_dir, "start.sh")), "start.sh is missing"

def test_status_endpoint():
    url = "http://127.0.0.1:8080/status"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

def test_build_endpoint_success():
    url = "http://127.0.0.1:8080/build"
    payload = {"version": "1.5.2", "constraint": ">= 1.5.0", "target": "ios"}
    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

def test_build_endpoint_failure():
    url = "http://127.0.0.1:8080/build"
    payload = {"version": "1.4.9", "constraint": ">= 1.5.0", "target": "android"}
    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}. Response: {response.text}"
    try:
        json_data = response.json()
        assert json_data.get("error") == "version constraint not met", f"Expected error message 'version constraint not met', got {json_data.get('error')}"
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")