# test_final_state.py

import os
import subprocess
import json
import time
import pytest
import requests

def get_total_frames(video_path):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-count_frames",
        "-show_entries", "stream=nb_read_frames",
        "-of", "default=nokey=1:noprint_wrappers=1",
        video_path
    ]
    try:
        output = subprocess.check_output(cmd, text=True).strip()
        return int(output)
    except Exception:
        # Fallback if nb_read_frames fails
        return len([f for f in os.listdir("/home/user/frames") if f.endswith(".jpg")])

def test_api_stats():
    video_path = "/app/experiment.mp4"
    assert os.path.exists(video_path), "Video file missing"

    expected_frames = get_total_frames(video_path)
    expected_events = 35

    url = "http://127.0.0.1:9090/api/stats"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "total_frames" in data, "Missing 'total_frames' in response"
    assert "total_events" in data, "Missing 'total_events' in response"

    assert data["total_frames"] == expected_frames, f"Expected {expected_frames} frames, got {data['total_frames']}"
    assert data["total_events"] == expected_events, f"Expected {expected_events} events, got {data['total_events']}"

def test_api_frames():
    # Test retrieving a specific frame
    frame_id = "10.jpg"
    url = f"http://127.0.0.1:9090/api/frames/{frame_id}"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert response.headers.get("Content-Type") in ["image/jpeg", "image/jpg"], f"Expected JPEG content type, got {response.headers.get('Content-Type')}"

    # Check if it's a valid JPEG by checking magic numbers
    content = response.content
    assert len(content) > 0, "Empty response body"
    assert content.startswith(b'\xff\xd8'), "Response body is not a valid JPEG"

def test_serve_directory():
    serve_dir = "/home/user/serve"
    assert os.path.exists(serve_dir), f"Serve directory {serve_dir} is missing"

    # Check if there are JPEGs in the serve directory
    files = []
    if os.path.isdir(serve_dir):
        files = [f for f in os.listdir(serve_dir) if f.endswith(".jpg")]

    assert len(files) > 0, f"No JPEG files found in {serve_dir}"