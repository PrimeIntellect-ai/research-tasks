# test_final_state.py

import os
import re
import subprocess
import requests
import json
import time

def get_expected_timestamp(frame_index):
    """Run ffprobe to get the expected timestamp for a given frame index."""
    video_path = "/app/data/surveillance.mp4"
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "frame=pts_time",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"ffprobe failed: {result.stderr}"

    lines = result.stdout.strip().split("\n")
    if frame_index < len(lines):
        return float(lines[frame_index])
    return None

def test_bashrc_env_var():
    """Check that PIPELINE_STRICT=1 is in ~/.bashrc"""
    bashrc_path = os.path.expanduser("~/.bashrc")
    assert os.path.exists(bashrc_path), f"{bashrc_path} does not exist"
    with open(bashrc_path, "r") as f:
        content = f.read()
    assert re.search(r"PIPELINE_STRICT=1", content), "PIPELINE_STRICT=1 not found in ~/.bashrc"

def test_timestamps_header():
    """Check that timestamps.h exists and has the correct format."""
    header_path = "/home/user/analytics/src/timestamps.h"
    assert os.path.exists(header_path), f"{header_path} does not exist"
    with open(header_path, "r") as f:
        content = f.read()
    assert "const double frame_timestamps[]" in content, "Array declaration not found in timestamps.h"
    assert "{" in content and "}" in content, "Array braces not found in timestamps.h"

def test_backend_files_exist():
    """Check that the C backend source and executable exist."""
    assert os.path.exists("/home/user/analytics/src/backend.c"), "backend.c source not found"
    assert os.path.exists("/home/user/analytics/backend"), "backend executable not found"
    assert os.access("/home/user/analytics/backend", os.X_OK), "backend is not executable"

def test_nginx_files_exist():
    """Check that Nginx config and certs exist."""
    assert os.path.exists("/home/user/analytics/nginx.conf"), "nginx.conf not found"
    assert os.path.exists("/home/user/analytics/certs/server.crt"), "TLS certificate not found"
    assert os.path.exists("/home/user/analytics/certs/server.key"), "TLS private key not found"

def test_processes_running():
    """Check that backend and nginx processes are running."""
    ps_cmd = subprocess.run(["ps", "-ef"], capture_output=True, text=True)
    assert "nginx" in ps_cmd.stdout, "nginx process is not running"
    assert "backend" in ps_cmd.stdout, "backend process is not running"

def test_http_backend_endpoint():
    """Verify the C backend responds correctly on HTTP port 9000."""
    expected_time = get_expected_timestamp(10)
    assert expected_time is not None, "Video does not have at least 11 frames"

    url = "http://127.0.0.1:9000/api/time?frame=10"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to backend at {url}: {e}"

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    try:
        data = response.json()
    except json.JSONDecodeError:
        assert False, f"Response is not valid JSON: {response.text}"

    assert "frame" in data and "time" in data, "JSON payload missing 'frame' or 'time' keys"
    assert data["frame"] == 10, f"Expected frame 10, got {data['frame']}"
    assert abs(float(data["time"]) - expected_time) < 0.001, f"Expected time {expected_time}, got {data['time']}"

def test_https_nginx_endpoint():
    """Verify Nginx proxies correctly on HTTPS port 8443."""
    expected_time = get_expected_timestamp(10)
    assert expected_time is not None, "Video does not have at least 11 frames"

    url = "https://127.0.0.1:8443/api/time?frame=10"
    try:
        response = requests.get(url, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to Nginx at {url}: {e}"

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    try:
        data = response.json()
    except json.JSONDecodeError:
        assert False, f"Response is not valid JSON: {response.text}"

    assert "frame" in data and "time" in data, "JSON payload missing 'frame' or 'time' keys"
    assert data["frame"] == 10, f"Expected frame 10, got {data['frame']}"
    assert abs(float(data["time"]) - expected_time) < 0.001, f"Expected time {expected_time}, got {data['time']}"

def test_https_nginx_404():
    """Verify out-of-bounds frame returns 404 on HTTPS port 8443."""
    url = "https://127.0.0.1:8443/api/time?frame=999999"
    try:
        response = requests.get(url, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to Nginx at {url}: {e}"

    assert response.status_code == 404, f"Expected status 404 for out-of-bounds frame, got {response.status_code}"