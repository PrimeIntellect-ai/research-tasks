# test_final_state.py

import os
import json
import hashlib
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"

def get_file_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def test_fast_tar_built():
    binary_path = "/app/vendored/fast-tar/fast-tar"
    assert os.path.isfile(binary_path), f"The fast-tar binary was not built at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"The fast-tar binary at {binary_path} is not executable"

def test_index_json_on_disk():
    index_path = "/home/user/index.json"
    assert os.path.isfile(index_path), f"{index_path} does not exist"

    with open(index_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{index_path} is not valid JSON")

    assert "files" in data, "JSON missing 'files' key"

    expected_files = {
        "sales/Q1.csv": get_file_sha256("/home/user/raw_data/sales/Q1.csv"),
        "users.xml": get_file_sha256("/home/user/raw_data/users.xml")
    }

    actual_files = {item.get("path"): item.get("hash") for item in data["files"]}

    for path, expected_hash in expected_files.items():
        assert path in actual_files, f"File {path} missing from index.json"
        assert actual_files[path] == expected_hash, f"Hash mismatch for {path} in index.json"

def test_backup_ftar_on_disk():
    backup_path = "/home/user/backup.ftar"
    assert os.path.isfile(backup_path), f"{backup_path} does not exist"
    assert os.path.getsize(backup_path) > 0, f"{backup_path} is empty"

def test_server_ping():
    try:
        response = requests.get(f"{BASE_URL}/ping", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/ping: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert response.text.strip() == "pong", f"Expected body 'pong', got '{response.text}'"

def test_server_index():
    try:
        response = requests.get(f"{BASE_URL}/index", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/index: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /index is not valid JSON")

    assert "files" in data, "JSON response missing 'files' key"

    expected_files = {
        "sales/Q1.csv": get_file_sha256("/home/user/raw_data/sales/Q1.csv"),
        "users.xml": get_file_sha256("/home/user/raw_data/users.xml")
    }

    actual_files = {item.get("path"): item.get("hash") for item in data["files"]}

    for path, expected_hash in expected_files.items():
        assert path in actual_files, f"File {path} missing from /index response"
        assert actual_files[path] == expected_hash, f"Hash mismatch for {path} in /index response"

def test_server_download():
    try:
        response = requests.get(f"{BASE_URL}/download", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/download: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    content_type = response.headers.get("Content-Type", "")
    assert "application/octet-stream" in content_type, f"Expected Content-Type application/octet-stream, got '{content_type}'"

    assert len(response.content) > 0, "Response body from /download is empty"

    # Compare with the local file
    backup_path = "/home/user/backup.ftar"
    if os.path.exists(backup_path):
        with open(backup_path, 'rb') as f:
            local_content = f.read()
        assert response.content == local_content, "Downloaded content does not match /home/user/backup.ftar"