# test_final_state.py

import os
import requests
import pytest

def test_project_data_extracted():
    path = "/home/user/assets/project_data.txt"
    assert os.path.exists(path), f"File missing: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert content == "LEGACY_PROJECT_IDENTIFIER_9942", f"Incorrect content in {path}"

def test_thumb_raw_exists():
    path = "/home/user/assets/thumb_raw.jpg"
    assert os.path.exists(path), f"File missing: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"
    assert os.path.getsize(path) > 0, f"File is empty: {path}"

def test_symlink_exists():
    symlink_path = "/home/user/public/thumb.jpg"
    target_path = "/home/user/assets/thumb_raw.jpg"
    assert os.path.exists(symlink_path), f"Symlink missing: {symlink_path}"
    assert os.path.islink(symlink_path), f"Not a symlink: {symlink_path}"
    assert os.readlink(symlink_path) == target_path, f"Symlink points to wrong target: {os.readlink(symlink_path)}"

def test_server_data_endpoint():
    try:
        response = requests.get("http://127.0.0.1:8080/data", timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Go server at /data: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    assert response.text == "LEGACY_PROJECT_IDENTIFIER_9942", f"Incorrect response body: {response.text}"

def test_server_video_thumb_endpoint():
    try:
        response = requests.get("http://127.0.0.1:8080/video-thumb", timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Go server at /video-thumb: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    assert "image/jpeg" in response.headers.get("Content-Type", ""), f"Expected Content-Type image/jpeg, got {response.headers.get('Content-Type')}"

    thumb_path = "/home/user/assets/thumb_raw.jpg"
    assert os.path.exists(thumb_path), "Raw thumb image missing"
    with open(thumb_path, "rb") as f:
        expected_bytes = f.read()

    assert response.content == expected_bytes, "Response content does not match the actual thumb_raw.jpg file"