# test_final_state.py

import os
import subprocess
import pytest
import requests

def get_frame_means(video_path, num_frames=3):
    cmd_probe = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=s=x:p=0", video_path
    ]
    try:
        output = subprocess.check_output(cmd_probe).decode('utf-8').strip()
        width, height = map(int, output.split('x'))
    except Exception as e:
        pytest.fail(f"Failed to probe video dimensions using ffprobe: {e}")

    cmd_ffmpeg = [
        "ffmpeg", "-i", video_path, "-vframes", str(num_frames),
        "-f", "image2pipe", "-pix_fmt", "gray", "-vcodec", "rawvideo", "-"
    ]
    try:
        raw_video = subprocess.check_output(cmd_ffmpeg, stderr=subprocess.DEVNULL)
    except Exception as e:
        pytest.fail(f"Failed to extract frames using ffmpeg: {e}")

    frame_size = width * height
    means = []
    for i in range(num_frames):
        frame_bytes = raw_video[i*frame_size : (i+1)*frame_size]
        if not frame_bytes:
            break
        mean_val = sum(frame_bytes) / frame_size
        means.append(mean_val)
    return means

def test_unauthorized_access():
    """Test that requests without the correct Authorization header return 401."""
    url = "http://127.0.0.1:8080/api/v1/telemetry"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_authorized_access_and_data_correctness():
    """Test that authorized requests return the correct JSON structure and values."""
    video_path = "/app/traffic_feed.mp4"
    if not os.path.exists(video_path):
        pytest.fail(f"Video file {video_path} does not exist.")

    means = get_frame_means(video_path, num_frames=3)
    if len(means) < 3:
        pytest.fail("Could not extract 3 frames from the video.")

    rolling_avgs = []
    for i in range(len(means)):
        window = means[max(0, i-4):i+1]
        rolling_avgs.append(sum(window) / len(window))

    timestamps = [
        "2024-05-01T08:00:00.000Z",
        "2024-05-01T08:00:00.040Z",
        "2024-05-01T08:00:00.080Z"
    ]

    expected_data = []
    for i in range(3):
        expected_data.append({
            "timestamp": timestamps[i],
            "metric": "brightness",
            "value": round(means[i], 2)
        })
        expected_data.append({
            "timestamp": timestamps[i],
            "metric": "rolling_avg",
            "value": round(rolling_avgs[i], 2)
        })

    # Sort as required: chronologically by timestamp, then alphabetically by metric name
    expected_data.sort(key=lambda x: (x["timestamp"], x["metric"]))

    url = "http://127.0.0.1:8080/api/v1/telemetry"
    params = {
        "start": "2024-05-01T08:00:00.000Z",
        "end": "2024-05-01T08:00:00.080Z"
    }
    headers = {
        "Authorization": "Bearer TRL-992-DATA"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        actual_data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert isinstance(actual_data, list), "Expected response to be a JSON array."
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual.get("timestamp") == expected["timestamp"], f"Record {i}: Expected timestamp {expected['timestamp']}, got {actual.get('timestamp')}"
        assert actual.get("metric") == expected["metric"], f"Record {i}: Expected metric {expected['metric']}, got {actual.get('metric')}"
        assert actual.get("value") == expected["value"], f"Record {i}: Expected value {expected['value']}, got {actual.get('value')}"