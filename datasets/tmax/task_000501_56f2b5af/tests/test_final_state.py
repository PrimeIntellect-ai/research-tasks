# test_final_state.py

import os
import re
import math
import pytest
import requests
from PIL import Image

API_BASE_URL = "http://127.0.0.1:8080/api/v1/frame"
AUTH_HEADER = {"Authorization": "Bearer secret-video-token"}

def test_pipeline_status_log():
    log_path = "/home/user/pipeline_status.log"
    assert os.path.exists(log_path), f"Log file missing: {log_path}"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert re.match(r"^Total frames processed: \d+$", content), f"Invalid log content: {content}"

def test_frames_extracted():
    frames_dir = "/home/user/frames"
    assert os.path.exists(frames_dir), f"Frames directory missing: {frames_dir}"
    frames = [f for f in os.listdir(frames_dir) if f.startswith("frame_") and f.endswith(".jpg")]
    assert len(frames) > 0, "No frames extracted"

def test_api_auth_missing():
    resp = requests.get(f"{API_BASE_URL}/1")
    assert resp.status_code == 401, f"Expected 401 for missing auth, got {resp.status_code}"

def test_api_auth_invalid():
    resp = requests.get(f"{API_BASE_URL}/1", headers={"Authorization": "Bearer wrong-token"})
    assert resp.status_code == 401, f"Expected 401 for invalid auth, got {resp.status_code}"

def test_api_404_not_found():
    resp = requests.get(f"{API_BASE_URL}/999999", headers=AUTH_HEADER)
    assert resp.status_code == 404, f"Expected 404 for non-existent frame, got {resp.status_code}"

def compute_frame_features(frame_id, frames_dir="/home/user/frames"):
    def get_brightness(fid):
        img_path = os.path.join(frames_dir, f"frame_{fid}.jpg")
        if not os.path.exists(img_path):
            return None
        img = Image.open(img_path).convert('L')
        pixels = list(img.getdata())
        return sum(pixels) / len(pixels)

    b_curr = get_brightness(frame_id)
    if b_curr is None:
        return None

    b_prev1 = get_brightness(frame_id - 1) if frame_id > 1 else None
    b_prev2 = get_brightness(frame_id - 2) if frame_id > 2 else None

    # Rolling avg for current frame
    vals = [b_curr]
    if b_prev1 is not None: vals.append(b_prev1)
    if b_prev2 is not None: vals.append(b_prev2)
    rolling_avg = sum(vals) / len(vals)

    # Rolling avg for previous frame
    is_flash = False
    if frame_id > 1:
        prev_vals = []
        if b_prev1 is not None: prev_vals.append(b_prev1)
        if b_prev2 is not None: prev_vals.append(b_prev2)
        b_prev3 = get_brightness(frame_id - 3) if frame_id > 3 else None
        if b_prev3 is not None: prev_vals.append(b_prev3)

        prev_rolling_avg = sum(prev_vals) / len(prev_vals)
        if b_curr > 1.5 * prev_rolling_avg:
            is_flash = True

    return {
        "brightness": round(b_curr, 2),
        "rolling_avg": round(rolling_avg, 2),
        "is_flash": is_flash
    }

def test_api_valid_frames():
    frames_dir = "/home/user/frames"
    frames = [f for f in os.listdir(frames_dir) if f.startswith("frame_") and f.endswith(".jpg")]
    total_frames = len(frames)
    if total_frames == 0:
        pytest.skip("No frames found to test API")

    test_ids = [1, min(5, total_frames), min(10, total_frames)]
    test_ids = list(set(test_ids))

    for fid in test_ids:
        expected = compute_frame_features(fid)
        assert expected is not None, f"Could not compute features for frame {fid}"

        resp = requests.get(f"{API_BASE_URL}/{fid}", headers=AUTH_HEADER)
        assert resp.status_code == 200, f"Expected 200 for frame {fid}, got {resp.status_code}"

        data = resp.json()
        assert "frame_id" in data
        assert data["frame_id"] == fid
        assert "brightness" in data
        assert "rolling_avg" in data
        assert "is_flash" in data

        assert math.isclose(data["brightness"], expected["brightness"], abs_tol=0.1), \
            f"Frame {fid} brightness mismatch. Expected {expected['brightness']}, got {data['brightness']}"
        assert math.isclose(data["rolling_avg"], expected["rolling_avg"], abs_tol=0.1), \
            f"Frame {fid} rolling_avg mismatch. Expected {expected['rolling_avg']}, got {data['rolling_avg']}"
        assert data["is_flash"] == expected["is_flash"], \
            f"Frame {fid} is_flash mismatch. Expected {expected['is_flash']}, got {data['is_flash']}"