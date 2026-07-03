# test_final_state.py

import os
import requests
import pytest

def test_directories_and_symlinks():
    """Verify that the required directories and symlinks exist."""
    extracted_frames_dir = "/home/user/extracted_frames"
    web_root_dir = "/home/user/web_root"
    media_symlink = "/home/user/web_root/media"

    assert os.path.isdir(extracted_frames_dir), f"Directory not found: {extracted_frames_dir}"
    assert os.path.isdir(web_root_dir), f"Directory not found: {web_root_dir}"
    assert os.path.islink(media_symlink), f"Symlink not found: {media_symlink}"
    assert os.readlink(media_symlink).rstrip('/') == extracted_frames_dir.rstrip('/'), f"Symlink {media_symlink} does not point to {extracted_frames_dir}"

def test_api_anomaly_unauthorized():
    """Verify that the /api/anomaly endpoint rejects unauthorized requests."""
    url = "http://127.0.0.1:8080/api/anomaly"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on 127.0.0.1:8080: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 Forbidden without auth, got {response.status_code}"

def test_api_anomaly_authorized():
    """Verify that the /api/anomaly endpoint returns the correct anomaly frame with valid auth."""
    url = "http://127.0.0.1:8080/api/anomaly"
    headers = {"Authorization": "Bearer syseng-secure-2024"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK with auth, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "anomaly_frame" in data, "Response JSON missing 'anomaly_frame' key"
    assert data["anomaly_frame"] == 142, f"Expected anomaly_frame to be 142, got {data['anomaly_frame']}"

def test_static_frame_serving():
    """Verify that Nginx serves the extracted frames correctly via the /static/ route."""
    # The spec mentions frame_0142.jpg as the expected format
    url = "http://127.0.0.1:8080/static/frame_0142.jpg"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for {url}, got {response.status_code}"
    assert response.headers.get("Content-Type", "").startswith("image/jpeg"), "Expected Content-Type to be image/jpeg"

    # Check magic bytes for JPEG
    assert response.content.startswith(b'\xff\xd8'), "Served file is not a valid JPEG image"