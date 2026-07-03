# test_final_state.py
import os
import struct
import requests
import pytest

WAL_PATH = "/app/db_system.wal"
FILTERED_WAL_PATH = "/home/user/filtered.wal"
FRAMES_DIR = "/home/user/frames"
BASE_URL = "http://127.0.0.1:8000"
AUTH_HEADER = {"Authorization": "Bearer archiver_token_x7z"}

def get_expected_wal_content():
    expected_records = [
        (1700000015, 0x03, b"OOM Killer invoked"),
        (1700000025, 0x03, b"Disk write failure sector 8")
    ]
    data = b""
    for ts, rtype, payload in expected_records:
        data += struct.pack('>Q B I', ts, rtype, len(payload))
        data += payload
    return data

def test_filtered_wal_exists_and_correct():
    assert os.path.exists(FILTERED_WAL_PATH), f"Filtered WAL file not found at {FILTERED_WAL_PATH}"
    with open(FILTERED_WAL_PATH, "rb") as f:
        content = f.read()
    assert content == get_expected_wal_content(), "Filtered WAL file content does not match expected critical records"

def test_frames_extracted():
    assert os.path.isdir(FRAMES_DIR), f"Frames directory not found at {FRAMES_DIR}"
    for sec in range(10, 16):
        frame_path = os.path.join(FRAMES_DIR, f"frame_{sec}.jpg")
        assert os.path.exists(frame_path), f"Frame for second {sec} not found at {frame_path}"
        assert os.path.getsize(frame_path) > 0, f"Frame for second {sec} is empty"

def test_api_wal_no_auth():
    try:
        resp = requests.get(f"{BASE_URL}/api/wal", timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")
    assert resp.status_code == 401, f"Expected HTTP 401 without auth, got {resp.status_code}"

def test_api_wal_with_auth():
    try:
        resp = requests.get(f"{BASE_URL}/api/wal", headers=AUTH_HEADER, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")
    assert resp.status_code == 200, f"Expected HTTP 200 with auth, got {resp.status_code}"
    assert resp.headers.get("Content-Type") == "application/octet-stream", "Incorrect Content-Type for WAL"
    assert resp.content == get_expected_wal_content(), "API returned incorrect WAL content"

def test_api_frame_with_auth():
    try:
        resp = requests.get(f"{BASE_URL}/api/frame/12", headers=AUTH_HEADER, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")
    assert resp.status_code == 200, f"Expected HTTP 200 with auth, got {resp.status_code}"
    assert resp.headers.get("Content-Type") == "image/jpeg", "Incorrect Content-Type for frame"
    assert resp.content.startswith(b"\xff\xd8"), "Response content does not appear to be a valid JPEG (missing magic bytes)"

def test_api_frame_not_found():
    try:
        resp = requests.get(f"{BASE_URL}/api/frame/99", headers=AUTH_HEADER, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")
    assert resp.status_code == 404, f"Expected HTTP 404 for missing frame, got {resp.status_code}"