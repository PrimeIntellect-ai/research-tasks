# test_final_state.py
import os
import json
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"
HEADERS = {"Authorization": "Bearer SECRET_DATA_TOKEN"}

def test_manifest_exists():
    manifest_path = "/home/user/manifest.json"
    assert os.path.exists(manifest_path), f"Manifest file missing at {manifest_path}"
    with open(manifest_path, 'r') as f:
        data = json.load(f)
    assert "summary" in data, "Manifest missing 'summary' key"
    assert "frames" in data, "Manifest missing 'frames' key"

    summary = data["summary"]
    assert "total_frames" in summary
    assert "black_frames" in summary
    assert "duplicate_frames" in summary
    assert "clean_frames" in summary

def test_server_auth_enforcement():
    # Missing header
    resp = requests.get(f"{BASE_URL}/summary")
    assert resp.status_code == 401, f"Expected 401 for missing auth, got {resp.status_code}"

    # Wrong header
    resp = requests.get(f"{BASE_URL}/summary", headers={"Authorization": "Bearer WRONG_TOKEN"})
    assert resp.status_code == 401, f"Expected 401 for wrong auth, got {resp.status_code}"

def test_server_summary_endpoint():
    resp = requests.get(f"{BASE_URL}/summary", headers=HEADERS)
    assert resp.status_code == 200, f"Expected 200 for /summary, got {resp.status_code}"
    data = resp.json()
    assert "total_frames" in data, "Summary response missing 'total_frames'"
    assert "black_frames" in data, "Summary response missing 'black_frames'"
    assert "duplicate_frames" in data, "Summary response missing 'duplicate_frames'"
    assert "clean_frames" in data, "Summary response missing 'clean_frames'"

    # Sanity check on values based on truth
    assert data["total_frames"] > 0, "Total frames should be greater than 0"

def test_server_frame_endpoints():
    # frame_0001.jpg should be clean
    resp = requests.get(f"{BASE_URL}/frame/frame_0001.jpg", headers=HEADERS)
    assert resp.status_code == 200, "Expected 200 for frame_0001.jpg"
    assert resp.json().get("status") == "clean", "frame_0001.jpg should be clean"

    # frame_0055.jpg should be black
    resp = requests.get(f"{BASE_URL}/frame/frame_0055.jpg", headers=HEADERS)
    if resp.status_code == 200:
        assert resp.json().get("status") == "black", "frame_0055.jpg should be black"

    # frame_0110.jpg should be duplicate
    resp = requests.get(f"{BASE_URL}/frame/frame_0110.jpg", headers=HEADERS)
    if resp.status_code == 200:
        assert resp.json().get("status") == "duplicate", "frame_0110.jpg should be duplicate"

def test_server_404_endpoint():
    resp = requests.get(f"{BASE_URL}/frame/nonexistent_frame_9999.jpg", headers=HEADERS)
    assert resp.status_code == 404, f"Expected 404 for nonexistent frame, got {resp.status_code}"