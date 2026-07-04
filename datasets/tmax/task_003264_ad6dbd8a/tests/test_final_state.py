# test_final_state.py

import os
import tarfile
import hashlib
import time
import requests
import subprocess
import pytest

def get_video_frame_count(filepath):
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-count_packets", "-show_entries", "stream=nb_read_packets",
        "-of", "csv=p=0", filepath
    ]
    try:
        output = subprocess.check_output(cmd, text=True).strip()
        return int(output)
    except Exception:
        return None

def test_video_info():
    """
    Test the GET /video_info endpoint to ensure it returns the correct total_frames.
    """
    url = "http://127.0.0.1:8080/video_info"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Response was not valid JSON")

    assert "total_frames" in data, "Response JSON missing 'total_frames' key"
    assert isinstance(data["total_frames"], int), "'total_frames' must be an integer"

    expected_frames = get_video_frame_count("/app/surveillance.mp4")
    if expected_frames is not None:
        assert data["total_frames"] == expected_frames, f"Expected {expected_frames} frames, got {data['total_frames']}"

def test_wal_processing():
    """
    Test the background watcher and GET /archived_wals endpoint.
    Drops a test tar.gz into /app/incoming/ and verifies correct processing.
    """
    os.makedirs("/app/incoming", exist_ok=True)
    os.makedirs("/app/archive", exist_ok=True)

    # Create valid WAL
    valid_content_base = b"MAGIC_WAL\ntxn 1\ntxn 2\n"
    valid_md5 = hashlib.md5(valid_content_base).hexdigest()
    valid_content = valid_content_base + f"END {valid_md5}".encode()

    # Create invalid WAL
    invalid_content = b"MAGIC_WAL\ntxn 1\nEND badmd5"

    valid_path = "/tmp/valid_test.wal"
    invalid_path = "/tmp/invalid_test.wal"

    with open(valid_path, "wb") as f:
        f.write(valid_content)
    with open(invalid_path, "wb") as f:
        f.write(invalid_content)

    tar_path = "/app/incoming/test_batch.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(valid_path, arcname="valid_test.wal")
        tar.add(invalid_path, arcname="invalid_test.wal")

    # Wait for the background task to process the file
    time.sleep(5)

    url = "http://127.0.0.1:8080/archived_wals"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Response was not valid JSON")

    assert "files" in data, "Response JSON missing 'files' key"
    files = data["files"]
    assert isinstance(files, list), "'files' must be a list"

    assert "valid_test_verified.wal" in files, "Valid WAL was not verified and archived"
    assert "invalid_test_verified.wal" not in files, "Invalid WAL was incorrectly archived"