# test_final_state.py

import os
import requests
import pytest

def test_analyzer_built():
    analyzer_path = "/home/user/src/analyzer"
    assert os.path.exists(analyzer_path), f"The compiled binary {analyzer_path} does not exist."
    assert os.access(analyzer_path, os.X_OK), f"The file {analyzer_path} is not executable."

def test_frames_extracted():
    for i in range(1, 31):
        frame_path = f"/home/user/frames/frame_{i:02d}.png"
        assert os.path.exists(frame_path), f"Frame {frame_path} does not exist. Did you extract all 30 frames correctly?"
        assert os.path.isfile(frame_path), f"Path {frame_path} is not a file."
        assert os.path.getsize(frame_path) > 0, f"Frame {frame_path} is empty."

def test_http_server_frame_14():
    url = "http://127.0.0.1:8080/analyze?frame=14"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request to {url} failed. Is the server running and listening on port 8080? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP status code 200, got {response.status_code}. Response: {response.text}"
    assert "RESULT_SCORE_84" in response.text, f"Expected 'RESULT_SCORE_84' in response body for frame 14, got: {response.text}"

def test_http_server_frame_05():
    url = "http://127.0.0.1:8080/analyze?frame=05"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request to {url} failed. Is the server running and listening on port 8080? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP status code 200, got {response.status_code}. Response: {response.text}"
    assert "RESULT_SCORE_10" in response.text, f"Expected 'RESULT_SCORE_10' in response body for frame 05, got: {response.text}"