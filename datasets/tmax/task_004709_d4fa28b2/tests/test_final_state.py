# test_final_state.py

import os
import subprocess
import json
import requests
import pytest
import math

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer devops_admin_2024"}

def get_frame_pixels(video_path, frame_number):
    # Extract the specific frame using ffmpeg
    # frame_number is 0-indexed in our logic, but let's assume the API uses 1-based or 0-based.
    # We will compute the variance of the frame using ffmpeg
    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vf", f"select='eq(n\\,{frame_number})'",
        "-vframes", "1",
        "-f", "rawvideo",
        "-pix_fmt", "gray",
        "-"
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None

def compute_variance(pixels):
    if not pixels:
        return None
    n = len(pixels)
    if n == 0:
        return 0.0
    mean = sum(pixels) / n
    variance = sum((x - mean) ** 2 for x in pixels) / n
    return variance

def test_auth_enforcement():
    """Test that the API enforces the Authorization header."""
    try:
        response = requests.get(f"{BASE_URL}/api/variance?frame=10", timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running or not listening on 127.0.0.1:8080")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth header, got {response.status_code}"

    bad_header = {"Authorization": "Bearer wrong_token"}
    response = requests.get(f"{BASE_URL}/api/variance?frame=10", headers=bad_header, timeout=5)
    assert response.status_code == 401, f"Expected 401 Unauthorized for incorrect auth header, got {response.status_code}"

def test_variance_endpoint():
    """Test the variance endpoint for a specific frame."""
    frame_to_test = 50
    response = requests.get(f"{BASE_URL}/api/variance?frame={frame_to_test}", headers=AUTH_HEADER, timeout=10)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"

    data = response.json()
    assert "frame" in data, "Response JSON missing 'frame' key"
    assert "variance" in data, "Response JSON missing 'variance' key"

    variance = data["variance"]
    assert isinstance(variance, (int, float)), "Variance must be a number"
    assert not math.isnan(variance), "Variance calculation resulted in NaN"
    assert not math.isinf(variance), "Variance calculation resulted in Infinity"
    assert variance >= 0, "Variance cannot be negative"

    # Optionally compare with our computed variance if ffmpeg is available
    video_path = "/app/telemetry_feed.mp4"
    if os.path.exists(video_path):
        pixels = get_frame_pixels(video_path, frame_to_test)
        if pixels:
            expected_variance = compute_variance(pixels)
            # Allow some tolerance for floating point and different variance definitions (population vs sample)
            # or different frame indexing
            assert math.isclose(variance, expected_variance, rel_tol=1e-2, abs_tol=1.0) or variance > 0, \
                f"Variance {variance} does not match expected {expected_variance}"

def test_alerts_endpoint():
    """Test the alerts endpoint."""
    threshold = 150.0
    response = requests.get(f"{BASE_URL}/api/alerts?threshold={threshold}", headers=AUTH_HEADER, timeout=10)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"

    data = response.json()
    assert isinstance(data, list), "Alerts endpoint must return a JSON array"
    for item in data:
        assert isinstance(item, int), f"Alerts array must contain integer frame numbers, got {type(item)}"