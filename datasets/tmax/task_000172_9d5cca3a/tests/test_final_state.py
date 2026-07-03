# test_final_state.py

import os
import json
import time
import pytest
import requests

def test_makefile_fixed():
    """Ensure the Makefile typo has been fixed."""
    makefile_path = "/app/bash-conf-tracker/Makefile"
    assert os.path.isfile(makefile_path), "Makefile is missing."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "/user/bin/" not in content, "Makefile still contains the typo '/user/bin/'."
    assert "/usr/local/bin" in content or "/usr/bin" in content, "Makefile does not contain a valid installation path."

def test_normalize_sh_fixed():
    """Ensure the normalize.sh bug has been fixed."""
    normalize_path = "/app/bash-conf-tracker/normalize.sh"
    assert os.path.isfile(normalize_path), "normalize.sh is missing."
    with open(normalize_path, "r") as f:
        content = f.read()
    assert "|| [ -n" in content or "|| [[ -n" in content or "|| [ ! -z" in content or "|| [[ ! -z" in content, \
        "The normalize.sh script does not contain the fix for the read loop (e.g., || [ -n \"$line\" ])."

def test_service_running_and_processing():
    """Test the running service to ensure it processes data correctly."""
    base_url = "http://127.0.0.1:9090"

    # Wait briefly for service to be available if it just started
    for _ in range(5):
        try:
            requests.get(f"{base_url}/")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)

    payload = 'OS=Ubuntu\nVERSION="22.04"\n hostname = db-server-01 \nOS = Debian\nAPP_ENV=production'

    try:
        post_response = requests.post(f"{base_url}/upload", data=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 127.0.0.1:9090 or not accepting connections.")

    assert post_response.status_code in (200, 201), f"Expected successful upload, got {post_response.status_code}"

    # Check if the file was created and contains the correct JSON
    config_file = "/home/user/configs/db-server-01.json"
    assert os.path.isfile(config_file), f"Config file {config_file} was not created."

    with open(config_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Config file does not contain valid JSON.")

    expected_data = {
        "os": "Debian",
        "version": "22.04",
        "hostname": "db-server-01",
        "app_env": "production"
    }

    for k, v in expected_data.items():
        assert data.get(k) == v, f"Expected key '{k}' to be '{v}', got '{data.get(k)}'"

def test_service_get_endpoint():
    """Test the GET endpoint returns the correct JSON."""
    url = "http://127.0.0.1:9090/config?host=db-server-01"
    response = requests.get(url, timeout=5)
    assert response.status_code == 200, f"Expected GET to return 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail("GET response is not valid JSON.")

    assert data.get("hostname") == "db-server-01", "GET response JSON does not contain correct hostname."

def test_service_missing_hostname():
    """Test that missing hostname returns 400 Bad Request."""
    url = "http://127.0.0.1:9090/upload"
    payload = "OS=Ubuntu\nAPP_ENV=production"
    response = requests.post(url, data=payload, timeout=5)
    assert response.status_code == 400, f"Expected POST without hostname to return 400, got {response.status_code}"