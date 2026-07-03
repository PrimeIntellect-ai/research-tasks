# test_final_state.py

import subprocess
import requests
import pytest
import time

BASE_URL = "http://127.0.0.1:9090"
VIDEO_PATH = "/app/security_cam.mp4"

def wait_for_server(url, timeout=5):
    """Wait for the server to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    return False

@pytest.fixture(scope="module", autouse=True)
def setup_server():
    """Ensure the server is running before tests."""
    assert wait_for_server(f"{BASE_URL}/ping"), f"Server at {BASE_URL} is not responding."

def test_ping_endpoint():
    """Test the /ping endpoint."""
    response = requests.get(f"{BASE_URL}/ping")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert response.text.strip() == "pong", f"Expected 'pong', got '{response.text}'"

def test_timestamps_endpoint():
    """Test the /api/timestamps endpoint."""
    response = requests.get(f"{BASE_URL}/api/timestamps")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    expected_timestamps = "2.5,7.1,12.0,15.3,22.8"
    assert response.text.strip() == expected_timestamps, f"Expected '{expected_timestamps}', got '{response.text}'"

def get_expected_brightness(timestamp: float, video_path: str) -> int:
    """Calculate the expected brightness using ffmpeg."""
    cmd = [
        "ffmpeg", "-ss", str(timestamp), "-i", video_path,
        "-vframes", "1", "-f", "image2pipe", "-vcodec", "rawvideo", "-pix_fmt", "gray", "-"
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    data = result.stdout
    if not data:
        return 0
    return sum(data) // len(data)

@pytest.mark.parametrize("timestamp", [2.5, 7.1, 15.3])
def test_frame_brightness_endpoint(timestamp):
    """Test the /api/frame_brightness endpoint with different timestamps."""
    response = requests.get(f"{BASE_URL}/api/frame_brightness?time={timestamp}")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    expected_brightness = get_expected_brightness(timestamp, VIDEO_PATH)
    actual_brightness = response.text.strip()

    assert actual_brightness == str(expected_brightness), f"For time {timestamp}, expected brightness {expected_brightness}, got {actual_brightness}"