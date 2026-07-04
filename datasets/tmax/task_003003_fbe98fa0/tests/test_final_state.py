# test_final_state.py

import os
import json
import glob
import time
import urllib.request
import urllib.error
import pytest

def test_video_stats_json():
    """Check that video_stats.json exists and contains the correct frame count."""
    stats_path = "/home/user/video_stats.json"
    assert os.path.isfile(stats_path), f"{stats_path} is missing. The extract script may not have been run or failed."

    with open(stats_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{stats_path} is not valid JSON.")

    assert "frame_count" in data, f"'frame_count' key missing in {stats_path}"
    assert data["frame_count"] == 142, f"Expected 142 frames, got {data['frame_count']}. Frame extraction or analysis failed."

def post_json(url, payload_path):
    """POST a JSON payload to the server, handling 429 rate limits."""
    with open(payload_path, "rb") as f:
        data = f.read()

    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

    max_retries = 20
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(0.5)
                continue
            return e.code
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to server at {url}: {e.reason}. Is the Go server running?")

    pytest.fail(f"Server returned 429 too many times for {payload_path}. Rate limiting might be too strict or blocking indefinitely.")

def test_adversarial_corpus():
    """Verify that the server correctly processes the clean and evil corpora."""
    url = "http://localhost:8080/validate"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, f"No clean files found in {clean_dir}."
    assert len(evil_files) > 0, f"No evil files found in {evil_dir}."

    clean_failed = []
    for cf in clean_files:
        status = post_json(url, cf)
        if status != 200:
            clean_failed.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        status = post_json(url, ef)
        if status != 400:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))