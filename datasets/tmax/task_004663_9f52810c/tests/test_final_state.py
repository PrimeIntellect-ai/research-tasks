# test_final_state.py

import json
import zlib
import subprocess
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"
VIDEO_PATH = "/app/test_feed.mp4"

def get_expected_frame_data(frame_index_1_based):
    """
    Computes the expected crc32 and luma_sum using ffmpeg.
    frame_index_1_based: 1-indexed frame number.
    """
    n_index = frame_index_1_based - 1

    cmd = [
        "ffmpeg",
        "-i", VIDEO_PATH,
        "-vf", f"select=eq(n\\,{n_index})",
        "-vframes", "1",
        "-pix_fmt", "gray",
        "-f", "image2pipe",
        "-vcodec", "rawvideo",
        "-"
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.returncode == 0, f"ffmpeg failed: {result.stderr.decode()}"

    raw_bytes = result.stdout
    assert len(raw_bytes) > 0, "ffmpeg returned empty raw bytes for the frame."

    expected_crc32 = zlib.crc32(raw_bytes)
    expected_luma_sum = sum(raw_bytes)

    return expected_crc32, expected_luma_sum

def test_analyze_frame_1():
    expected_crc, expected_luma = get_expected_frame_data(1)

    try:
        response = requests.get(f"{BASE_URL}/analyze?frame=1", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to /analyze?frame=1: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type: application/json"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "frame" in data, "Missing 'frame' in response"
    assert "crc32" in data, "Missing 'crc32' in response"
    assert "luma_sum" in data, "Missing 'luma_sum' in response"

    assert data["frame"] == 1, f"Expected frame 1, got {data['frame']}"
    assert data["crc32"] == expected_crc, f"Expected crc32 {expected_crc}, got {data['crc32']}"
    assert data["luma_sum"] == expected_luma, f"Expected luma_sum {expected_luma}, got {data['luma_sum']}"

def test_analyze_frame_15():
    expected_crc, expected_luma = get_expected_frame_data(15)

    try:
        response = requests.get(f"{BASE_URL}/analyze?frame=15", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to /analyze?frame=15: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type: application/json"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data["frame"] == 15, f"Expected frame 15, got {data['frame']}"
    assert data["crc32"] == expected_crc, f"Expected crc32 {expected_crc}, got {data['crc32']}"
    assert data["luma_sum"] == expected_luma, f"Expected luma_sum {expected_luma}, got {data['luma_sum']}"

def test_benchmark():
    try:
        response = requests.get(f"{BASE_URL}/benchmark", timeout=15)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to /benchmark: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type: application/json"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "frames_processed" in data, "Missing 'frames_processed' in response"
    assert "time_ms" in data, "Missing 'time_ms' in response"

    assert data["frames_processed"] == 5, f"Expected frames_processed to be 5, got {data['frames_processed']}"
    assert isinstance(data["time_ms"], (int, float)), "time_ms must be a number"
    assert data["time_ms"] > 0, f"Expected time_ms to be > 0, got {data['time_ms']}"