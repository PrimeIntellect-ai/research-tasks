# test_final_state.py

import os
import sqlite3
import json
import pytest
import requests

FRAMES_DIR = "/home/user/frames"
CORRUPTED_LOG = "/home/user/corrupted_frames.log"
DB_PATH = "/home/user/features.db"
SERVICE_URL = "http://127.0.0.1:8080/search"

def test_frames_extracted_and_cleaned():
    """Verify that frames were extracted and corrupted ones were deleted."""
    assert os.path.isdir(FRAMES_DIR), f"Directory {FRAMES_DIR} does not exist."

    files = set(os.listdir(FRAMES_DIR))

    # 60 frames total, 4 deleted
    expected_missing = {"frame_0012.jpg", "frame_0013.jpg", "frame_0014.jpg", "frame_0045.jpg"}

    for missing in expected_missing:
        assert missing not in files, f"Corrupted frame {missing} should have been deleted."

    assert len(files) == 56, f"Expected 56 frames, found {len(files)}."

    for i in range(1, 61):
        filename = f"frame_{i:04d}.jpg"
        if filename not in expected_missing:
            assert filename in files, f"Expected valid frame {filename} is missing."

def test_corrupted_frames_log():
    """Verify the corrupted_frames.log contains the correct filenames."""
    assert os.path.exists(CORRUPTED_LOG), f"Log file {CORRUPTED_LOG} does not exist."

    with open(CORRUPTED_LOG, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_missing = {"frame_0012.jpg", "frame_0013.jpg", "frame_0014.jpg", "frame_0045.jpg"}
    assert set(lines) == expected_missing, f"Log file contents {set(lines)} do not match expected {expected_missing}."

def test_sqlite_database():
    """Verify the SQLite database has the correct schema and row count."""
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='frame_features'")
    assert cursor.fetchone() is not None, "Table 'frame_features' does not exist."

    cursor.execute("SELECT COUNT(*) FROM frame_features")
    count = cursor.fetchone()[0]
    assert count == 56, f"Expected 56 rows in frame_features, found {count}."

    conn.close()

def test_service_unauthorized():
    """Verify the service returns 401 for an invalid token."""
    payload = {
        "target_frame": "frame_0005.jpg",
        "top_k": 2,
        "token": "bad-token"
    }
    try:
        response = requests.post(SERVICE_URL, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}."

def test_service_authorized_search():
    """Verify the service returns 200 and correct JSON structure for a valid request."""
    payload = {
        "target_frame": "frame_0005.jpg",
        "top_k": 2,
        "token": "data-sci-auth-77"
    }
    try:
        response = requests.post(SERVICE_URL, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail("Response is not valid JSON.")

    assert "results" in data, "Response JSON missing 'results' key."
    results = data["results"]
    assert isinstance(results, list), "'results' should be a list."
    assert len(results) == 2, f"Expected 2 results, got {len(results)}."
    assert "frame_0005.jpg" not in results, "Target frame should not be in the results."