# test_final_state.py

import os
import tarfile
import requests
import pytest
import json

def test_fstab_addition():
    fstab_path = "/home/user/fstab_addition"
    assert os.path.exists(fstab_path), f"File {fstab_path} does not exist."
    with open(fstab_path, "r") as f:
        content = f.read().strip()
    expected = "cold-vault.internal:/data /mnt/archive nfs defaults,ro 0 0"
    assert content == expected, f"fstab_addition content is incorrect. Got: {content}"

def test_cold_storage_tarball():
    tarball_path = "/home/user/cold_storage.tar.gz"
    assert os.path.exists(tarball_path), f"Tarball {tarball_path} does not exist."
    assert tarfile.is_tarfile(tarball_path), f"File {tarball_path} is not a valid tar archive."

def test_http_server_valid_auth():
    url = "http://127.0.0.1:8080/report"
    headers = {"Authorization": "Bearer FinOpsSecure2024"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    assert data.get("archived_files_count") == 16, f"Expected 16 archived files, got {data.get('archived_files_count')}"
    assert data.get("archived_bytes") == 10240, f"Expected 10240 archived bytes, got {data.get('archived_bytes')}"
    assert data.get("status") == "optimized", f"Expected status 'optimized', got {data.get('status')}"

def test_http_server_invalid_auth():
    url = "http://127.0.0.1:8080/report"
    headers = {"Authorization": "Bearer WrongToken"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server: {e}")

    assert response.status_code == 401, f"Expected status code 401 for invalid token, got {response.status_code}"

def test_http_server_missing_auth():
    url = "http://127.0.0.1:8080/report"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server: {e}")

    assert response.status_code == 401, f"Expected status code 401 for missing token, got {response.status_code}"