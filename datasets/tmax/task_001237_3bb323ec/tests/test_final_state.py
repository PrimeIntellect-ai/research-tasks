# test_final_state.py
import os
import zipfile
import hashlib
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"

def test_status_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/status", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to GET /status: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /status is not valid JSON: {response.text}")

    assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"

def test_archives_clean_endpoint():
    try:
        response = requests.post(f"{BASE_URL}/archives/clean", timeout=15)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to POST /archives/clean: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /archives/clean is not valid JSON: {response.text}")

    assert isinstance(data, list), "Expected a JSON array of filenames"
    expected_files = {"backup_1.tar.gz", "metrics_1.tar.gz"}
    assert set(data) == expected_files, f"Expected {expected_files}, got {set(data)}"

    # Check filesystem state
    archives_dir = "/home/user/archives"
    assert os.path.exists(os.path.join(archives_dir, "backup_1.tar.gz")), "backup_1.tar.gz should not be deleted"
    assert os.path.exists(os.path.join(archives_dir, "metrics_1.tar.gz")), "metrics_1.tar.gz should not be deleted"
    assert os.path.exists(os.path.join(archives_dir, "random_1.tar.gz")), "random_1.tar.gz should not be deleted"

    assert not os.path.exists(os.path.join(archives_dir, "backup_2.tar.gz")), "Corrupt archive backup_2.tar.gz was not deleted"
    assert not os.path.exists(os.path.join(archives_dir, "old_data.tar.gz")), "Corrupt archive old_data.tar.gz was not deleted"

def test_logs_errors_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/logs/errors", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to GET /logs/errors: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    assert response.text.strip() == "2", f"Expected count '2', got '{response.text}'"

def test_video_extract_endpoint():
    try:
        response = requests.post(f"{BASE_URL}/video/extract", timeout=30)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to POST /video/extract: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    returned_hash = response.text.strip()

    zip_path = "/home/user/frame.zip"
    assert os.path.exists(zip_path), f"{zip_path} was not created"

    # Calculate actual SHA256 of the zip file
    sha256 = hashlib.sha256()
    with open(zip_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    actual_hash = sha256.hexdigest()

    assert returned_hash == actual_hash, f"Returned hash {returned_hash} does not match actual hash {actual_hash}"

    # Verify zip contents
    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        assert len(namelist) == 1, f"Expected exactly 1 file in zip, found {len(namelist)}: {namelist}"
        assert namelist[0] == "frame.jpg", f"Expected file 'frame.jpg' in zip, found '{namelist[0]}'"