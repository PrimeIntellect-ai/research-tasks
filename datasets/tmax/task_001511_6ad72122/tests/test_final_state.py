# test_final_state.py

import os
import hashlib
import requests
import pytest

AUTH_KEY = "KEY_B5x9_P!q2M"
SERVER_URL = "http://127.0.0.1:8080/manifest"

def get_expected_manifest():
    app1_content = b"server_ip=10.0.0.50\nmode=modern\nthreads=4\n"
    db_content = b"server_ip=10.0.0.101\nmode=modern\ncache=256M\n"

    app1_sha = hashlib.sha256(app1_content).hexdigest()
    db_sha = hashlib.sha256(db_content).hexdigest()

    # Sorted alphabetically by filename
    return f"app1.conf:{app1_sha}\ndb.conf:{db_sha}"

def test_extracted_configs_exist_and_modified():
    """Verify that the configs were extracted and modified correctly."""
    app1_path = "/home/user/extracted_configs/app1.conf"
    db_path = "/home/user/extracted_configs/db.conf"

    assert os.path.isfile(app1_path), f"Expected config file '{app1_path}' is missing."
    assert os.path.isfile(db_path), f"Expected config file '{db_path}' is missing."

    with open(app1_path, "rb") as f:
        app1_content = f.read()
    with open(db_path, "rb") as f:
        db_content = f.read()

    expected_app1 = b"server_ip=10.0.0.50\nmode=modern\nthreads=4\n"
    expected_db = b"server_ip=10.0.0.101\nmode=modern\ncache=256M\n"

    assert app1_content == expected_app1, f"Content of '{app1_path}' is incorrect. Expected: {expected_app1}, Got: {app1_content}"
    assert db_content == expected_db, f"Content of '{db_path}' is incorrect. Expected: {expected_db}, Got: {db_content}"

def test_server_unauthorized():
    """Verify that the server returns 401 Unauthorized when the auth header is missing."""
    try:
        response = requests.get(SERVER_URL, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {SERVER_URL}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for missing auth header, got {response.status_code}. Response: {response.text}"

def test_server_authorized_manifest():
    """Verify that the server returns 200 OK and the correct manifest when the auth header is present."""
    headers = {"X-Auth-Key": AUTH_KEY}
    try:
        response = requests.get(SERVER_URL, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {SERVER_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200 for valid auth header, got {response.status_code}. Response: {response.text}"

    expected_manifest = get_expected_manifest()
    actual_manifest = response.text.strip()

    assert actual_manifest == expected_manifest, f"Manifest content is incorrect.\nExpected:\n{expected_manifest}\n\nGot:\n{actual_manifest}"

def test_c_program_exists():
    """Verify that the C program and its compiled binary exist."""
    c_source = "/home/user/config_server.c"
    c_binary = "/home/user/config_server"

    assert os.path.isfile(c_source), f"Expected C source file '{c_source}' is missing."
    assert os.path.isfile(c_binary), f"Expected compiled binary '{c_binary}' is missing."
    assert os.access(c_binary, os.X_OK), f"Expected binary '{c_binary}' to be executable."