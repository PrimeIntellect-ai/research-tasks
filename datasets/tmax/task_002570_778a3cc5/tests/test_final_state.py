# test_final_state.py
import subprocess
import requests
import pytest
import os

def compute_expected_peak_frame(video_path):
    cmd = [
        'ffmpeg', '-i', video_path,
        '-f', 'image2pipe',
        '-pix_fmt', 'gray',
        '-vcodec', 'rawvideo', '-'
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    width = 320
    height = 240
    frame_size = width * height

    prev_frame = None
    max_diff = -1
    peak_frame_idx = -1
    current_idx = 1

    while True:
        raw_frame = process.stdout.read(frame_size)
        if not raw_frame or len(raw_frame) != frame_size:
            break

        if prev_frame is not None:
            diff = sum(abs(raw_frame[i] - prev_frame[i]) for i in range(frame_size))
            if diff > max_diff:
                max_diff = diff
                peak_frame_idx = current_idx

        prev_frame = raw_frame
        current_idx += 1

    return peak_frame_idx

def test_service_response():
    video_path = '/app/video.mp4'
    assert os.path.exists(video_path), f"Video file missing at {video_path}"

    # Compute ground truth using the reference logic
    expected_peak = compute_expected_peak_frame(video_path)

    url = "http://127.0.0.1:8080/api/peak_motion"
    headers = {"Authorization": "Bearer deploy_token_2024"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "peak_frame" in data, f"Response JSON missing 'peak_frame' key: {data}"

    actual_peak = data["peak_frame"]
    assert actual_peak == expected_peak, f"Expected peak_frame {expected_peak}, but got {actual_peak}"

def test_unauthorized_access():
    url = "http://127.0.0.1:8080/api/peak_motion"
    headers = {"Authorization": "Bearer wrong_token"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for bad token, got {response.status_code}"