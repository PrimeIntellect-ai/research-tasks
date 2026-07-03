# test_final_state.py

import os
import subprocess
import urllib.request
import pytest

def test_frames_extracted():
    """Verify that exactly 5 frames were extracted to the correct directory."""
    frames_dir = "/home/user/frames/"
    assert os.path.isdir(frames_dir), f"Frames directory {frames_dir} does not exist."

    jpg_files = [f for f in os.listdir(frames_dir) if f.endswith(".jpg")]
    assert len(jpg_files) == 5, f"Expected exactly 5 .jpg files in {frames_dir}, found {len(jpg_files)}."

def test_sanitizer_corpus():
    """Verify the sanitizer script against the clean and evil corpora."""
    sanitizer_path = "/home/user/edge_deploy/sanitizer.py"
    assert os.path.isfile(sanitizer_path), f"Sanitizer script is missing at {sanitizer_path}."

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."

    clean_failed = []
    evil_failed = []

    clean_files = os.listdir(clean_dir)
    evil_files = os.listdir(evil_dir)

    for f in clean_files:
        filepath = os.path.join(clean_dir, f)
        result = subprocess.run(["python3", sanitizer_path, filepath], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(f)

    for f in evil_files:
        filepath = os.path.join(evil_dir, f)
        result = subprocess.run(["python3", sanitizer_path, filepath], capture_output=True)
        if result.returncode == 0:
            evil_failed.append(f)

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_load_balancer():
    """Verify that the load balancer routes requests correctly to the backend servers."""
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/frame_1.jpg")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}."
            content = response.read()
            assert len(content) > 0, "The response content is empty."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to fetch frame_1.jpg via load balancer on port 8080: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error when testing load balancer: {e}")