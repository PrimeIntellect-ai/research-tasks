# test_final_state.py

import os
import glob
import urllib.request
import urllib.error
import subprocess
import pytest

def test_frame_count():
    """Verify that the frame count is correctly computed and written to frame_count.txt."""
    assert os.path.exists("/app/frame_count.txt"), "/app/frame_count.txt is missing"

    with open("/app/frame_count.txt", "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"frame_count.txt does not contain a valid integer: {content}"
    actual_count = int(content)

    # Derive the expected frame count based on the video duration (1 fps)
    try:
        cmd = [
            "ffprobe", 
            "-v", "error", 
            "-show_entries", "format=duration", 
            "-of", "default=noprint_wrappers=1:nokey=1", 
            "/app/incident.mp4"
        ]
        duration_str = subprocess.check_output(cmd, text=True).strip()
        expected_frames = int(float(duration_str))
    except Exception:
        # Fallback to the truth value from the spec if ffprobe fails or is unavailable
        expected_frames = 45

    # Allow a small margin of error due to rounding differences in extraction tools
    assert abs(actual_count - expected_frames) <= 2, f"Expected around {expected_frames} frames, but got {actual_count}"

def test_api_corpus():
    """Verify that the API correctly rejects evil patches and accepts clean patches."""
    evil_dir = "/app/tests/evil"
    clean_dir = "/app/tests/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*"))
    clean_files = glob.glob(os.path.join(clean_dir, "*"))

    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"
    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"

    evil_bypassed = []
    for fpath in evil_files:
        with open(fpath, "rb") as f:
            data = f.read()
        req = urllib.request.Request("http://localhost:8080/api/v1/patch", data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.getcode()
        except urllib.error.HTTPError as e:
            status = e.code
        except Exception as e:
            pytest.fail(f"API request failed for {fpath} (is the server running?): {e}")

        if status != 400:
            evil_bypassed.append(os.path.basename(fpath))

    clean_modified = []
    for fpath in clean_files:
        with open(fpath, "rb") as f:
            data = f.read()
        req = urllib.request.Request("http://localhost:8080/api/v1/patch", data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.getcode()
        except urllib.error.HTTPError as e:
            status = e.code
        except Exception as e:
            pytest.fail(f"API request failed for {fpath} (is the server running?): {e}")

        if status != 200:
            clean_modified.append(os.path.basename(fpath))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))