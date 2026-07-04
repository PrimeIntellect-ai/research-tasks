# test_final_state.py

import os
import requests
import pytest
import time

def test_base_conf_exists_and_correct():
    base_conf_path = "/home/user/configs/base.conf"
    assert os.path.isfile(base_conf_path), f"Missing base configuration file at {base_conf_path}"

    with open(base_conf_path, 'r') as f:
        content = f.read()

    assert "max_connections=500" in content, "base.conf missing parsed Key=Value for max_connections"
    assert "timeout=30s" in content, "base.conf missing parsed Key=Value for timeout"

def test_final_conf_exists_and_correct():
    final_conf_path = "/home/user/configs/final.conf"
    assert os.path.isfile(final_conf_path), f"Missing final configuration file at {final_conf_path}"

    with open(final_conf_path, 'r') as f:
        content = f.read()

    assert "max_connections=500" in content, "final.conf missing base.conf contents (max_connections)"
    assert "timeout=30s" in content, "final.conf missing base.conf contents (timeout)"
    assert "db_host=localhost" in content, "final.conf missing patch contents (db_host)"

def test_patches_extracted_and_renamed():
    patch_file_path = "/home/user/configs/patches/patch1/db/database.conf"
    assert os.path.isfile(patch_file_path), f"Renamed patch file not found at {patch_file_path}"

    tmp_file_path = "/home/user/configs/patches/patch1/db/database.conf.tmp"
    assert not os.path.exists(tmp_file_path), "Temporary patch file was not renamed"

def test_c_server_valid_authentication():
    url = "http://127.0.0.1:8080/api/config"
    headers = {"Authorization": "Bearer echo-bravo-niner-tango"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the C server on port 8080: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "text/plain" in response.headers.get("Content-Type", ""), "Expected Content-Type: text/plain"

    body = response.text
    assert "max_connections=500" in body, "Response body missing max_connections"
    assert "timeout=30s" in body, "Response body missing timeout"
    assert "db_host=localhost" in body, "Response body missing db_host"

def test_c_server_invalid_authentication():
    url = "http://127.0.0.1:8080/api/config"
    headers = {"Authorization": "Bearer wrong-token-123"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the C server on port 8080: {e}")

    assert response.status_code == 401, f"Expected status code 401 for invalid auth, got {response.status_code}"

def test_c_server_missing_authentication():
    url = "http://127.0.0.1:8080/api/config"

    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the C server on port 8080: {e}")

    assert response.status_code == 401, f"Expected status code 401 for missing auth, got {response.status_code}"