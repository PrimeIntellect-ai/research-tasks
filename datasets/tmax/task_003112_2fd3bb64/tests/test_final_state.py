# test_final_state.py
import os
import sqlite3
import time
import requests
import pytest

try:
    import cv2
    import numpy as np
except ImportError:
    pass  # Will be handled if needed, but agent should have installed it

BASE_URL = "http://127.0.0.1:8080"

def get_expected_brightness(video_path, frame_idx):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise ValueError(f"Could not read frame {frame_idx} from {video_path}")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return float(np.mean(gray))

def test_server_listening_and_bad_requests():
    # Test missing key
    resp = requests.post(f"{BASE_URL}/analyze", json={"wrong_key": 10})
    assert resp.status_code == 400, f"Expected 400 for missing 'frame' key, got {resp.status_code}"

    # Test negative frame
    resp = requests.post(f"{BASE_URL}/analyze", json={"frame": -5})
    assert resp.status_code == 400, f"Expected 400 for negative frame, got {resp.status_code}"

def test_rate_limiting_and_correctness():
    video_path = "/app/video.mp4"
    frame_idx = 5
    expected_brightness = get_expected_brightness(video_path, frame_idx)

    # We need to make 5 successful requests
    for i in range(5):
        resp = requests.post(f"{BASE_URL}/analyze", json={"frame": frame_idx})
        assert resp.status_code == 200, f"Expected 200 for valid request {i+1}, got {resp.status_code}"
        data = resp.json()
        assert "brightness" in data, "Response JSON missing 'brightness' key"
        assert abs(data["brightness"] - expected_brightness) < 0.1, \
            f"Expected brightness ~{expected_brightness}, got {data['brightness']}"

    # 6th request should be rate limited
    resp = requests.post(f"{BASE_URL}/analyze", json={"frame": frame_idx})
    assert resp.status_code == 429, f"Expected 429 for 6th request, got {resp.status_code}"

def test_database_state():
    db_path = "/app/metrics.db"
    assert os.path.isfile(db_path), f"Database file not found at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM metrics;")
    count = cursor.fetchone()[0]
    assert count == 5, f"Expected exactly 5 rows in metrics table, got {count}"

    cursor.execute("SELECT frame, brightness FROM metrics;")
    rows = cursor.fetchall()
    for row in rows:
        assert row[0] == 5, f"Expected frame to be 5, got {row[0]}"
        # Brightness should be close to expected, but we mainly check frame here
        assert isinstance(row[1], float), "Brightness should be a float"

    conn.close()