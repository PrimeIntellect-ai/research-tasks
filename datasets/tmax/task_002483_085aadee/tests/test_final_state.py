# test_final_state.py

import os
import requests
import pytest
import time

def test_extracted_files():
    base_dir = "/home/user/extracted"
    expected_files = ["config.json", "src/main.py", "assets/logo.png"]
    for f in expected_files:
        path = os.path.join(base_dir, f)
        assert os.path.isfile(path), f"Extracted file missing: {path}"

def test_backup_files():
    tarball = "/home/user/backup/latest.tar.gz"
    manifest = "/home/user/backup/manifest.txt"

    assert os.path.isfile(tarball), f"Backup tarball missing: {tarball}"
    assert os.path.isfile(manifest), f"Manifest missing: {manifest}"

def get_valid_token():
    # The transcript might result in different normalizations
    # We will test a few valid possibilities
    return ["DELTA 42", "DELTA42", "DELTA FORTY TWO"]

def test_http_service_unauthorized():
    url = "http://127.0.0.1:8080/files"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP service: {e}")

    assert response.status_code in (401, 403), f"Expected 401 or 403 for missing token, got {response.status_code}"

def test_http_service_endpoints():
    base_url = "http://127.0.0.1:8080"
    tokens = get_valid_token()

    # Find a working token
    working_token = None
    for token in tokens:
        headers = {"X-Project-Token": token}
        try:
            r = requests.get(f"{base_url}/files", headers=headers, timeout=2)
            if r.status_code == 200:
                working_token = token
                break
        except requests.exceptions.RequestException:
            pass

    assert working_token is not None, "Could not authenticate with any expected token variant (e.g., DELTA 42, DELTA42)"

    headers = {"X-Project-Token": working_token}

    # Test /files
    r_files = requests.get(f"{base_url}/files", headers=headers, timeout=2)
    assert r_files.status_code == 200
    data_files = r_files.json()
    assert "files" in data_files
    for expected in ["config.json", "src/main.py", "assets/logo.png"]:
        assert expected in data_files["files"], f"Missing {expected} in /files response"

    # Test /transcript
    r_transcript = requests.get(f"{base_url}/transcript", headers=headers, timeout=2)
    assert r_transcript.status_code == 200
    data_transcript = r_transcript.json()
    assert "transcript" in data_transcript
    assert len(data_transcript["transcript"]) > 0, "Transcript is empty"

    # Test /backup/status
    r_backup = requests.get(f"{base_url}/backup/status", headers=headers, timeout=2)
    assert r_backup.status_code == 200
    data_backup = r_backup.json()
    assert data_backup.get("backup_path") == "/home/user/backup/latest.tar.gz"
    assert data_backup.get("manifest_exists") is True