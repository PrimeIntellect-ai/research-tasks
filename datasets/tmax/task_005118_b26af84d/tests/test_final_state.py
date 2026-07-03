# test_final_state.py

import os
import stat
import pytest
import requests

def test_video_permissions():
    video_path = "/app/camera_01.mp4"
    assert os.path.exists(video_path), f"Video file missing at {video_path}"

    st = os.stat(video_path)
    # Check permissions: user rw (0o6), group 0, other 0
    # The mode should be exactly 0o600 or equivalent for user rw-, group ---, other ---
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o600, f"Expected permissions 0o600 (rw-------), but got {oct(permissions)}"

def test_deploy_script_exists_and_executable():
    script_path = "/home/user/deploy.sh"
    assert os.path.exists(script_path), f"Deployment script missing at {script_path}"
    assert os.path.isfile(script_path), f"Path {script_path} is not a file"
    assert os.access(script_path, os.X_OK), f"Deployment script {script_path} is not executable"

def test_api_unauthorized():
    url = "http://127.0.0.1:9042/api/v1/status"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API on 127.0.0.1:9042: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for missing token, got {response.status_code}"

def test_api_authorized():
    url = "http://127.0.0.1:9042/api/v1/status"
    headers = {"Authorization": "Bearer sec-token-8819"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API on 127.0.0.1:9042: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for valid token, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("API did not return valid JSON")

    assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"
    assert data.get("black_frames") == 5, f"Expected 5 black frames, got {data.get('black_frames')}"