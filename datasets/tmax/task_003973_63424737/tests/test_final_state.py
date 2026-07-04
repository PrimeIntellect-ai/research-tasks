# test_final_state.py

import os
import hashlib
import requests
import pytest

RESTORED_DIR = "/home/user/restored_data"
MANIFEST_PATH = os.path.join(RESTORED_DIR, "manifest.json")
DATA_CSV_PATH = os.path.join(RESTORED_DIR, "data.csv")
LOG_PATH = "/home/user/restore_drill.log"
SERVER_URL = "http://127.0.0.1:8080"

def test_log_file_exists():
    assert os.path.exists(LOG_PATH), f"Log file missing: {LOG_PATH}"
    assert os.path.isfile(LOG_PATH), f"Log path is not a file: {LOG_PATH}"

def test_restored_files_exist():
    assert os.path.exists(MANIFEST_PATH), f"Restored manifest missing: {MANIFEST_PATH}"
    assert os.path.exists(DATA_CSV_PATH), f"Restored data missing: {DATA_CSV_PATH}"

def test_http_server_auth_and_content():
    # Compute MD5 of the restored manifest.json
    with open(MANIFEST_PATH, "rb") as f:
        manifest_content = f.read()

    password = hashlib.md5(manifest_content).hexdigest()
    username = "backup_admin"

    # 1. Test without auth (should fail)
    try:
        resp_no_auth = requests.get(f"{SERVER_URL}/manifest.json", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {SERVER_URL}: {e}")

    assert resp_no_auth.status_code == 401, "Server did not require authentication (expected 401 Unauthorized)"

    # 2. Test with incorrect auth
    resp_bad_auth = requests.get(f"{SERVER_URL}/manifest.json", auth=(username, "wrongpassword"), timeout=5)
    assert resp_bad_auth.status_code == 401, "Server accepted invalid credentials"

    # 3. Test with correct auth
    resp_auth = requests.get(f"{SERVER_URL}/manifest.json", auth=(username, password), timeout=5)
    assert resp_auth.status_code == 200, f"Server rejected valid credentials, got status {resp_auth.status_code}"
    assert resp_auth.content == manifest_content, "Served manifest.json content does not match the file on disk"

    # 4. Test serving other files
    with open(DATA_CSV_PATH, "rb") as f:
        data_content = f.read()

    resp_data = requests.get(f"{SERVER_URL}/data.csv", auth=(username, password), timeout=5)
    assert resp_data.status_code == 200, f"Failed to fetch data.csv, got status {resp_data.status_code}"
    assert resp_data.content == data_content, "Served data.csv content does not match the file on disk"