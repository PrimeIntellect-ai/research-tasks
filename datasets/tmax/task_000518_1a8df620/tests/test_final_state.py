# test_final_state.py

import os
import json
import subprocess
import pytest
import sys

def test_ocr_extractor_installed():
    """Verify that the ocr_extractor package has been successfully installed."""
    try:
        # Check if the package can be imported
        result = subprocess.run(
            [sys.executable, "-c", "import ocr_extractor"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Failed to import ocr_extractor. Error: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Could not verify ocr_extractor installation: {e}")

def test_video_analysis_json():
    """Verify the contents of /home/user/video_analysis.json"""
    json_path = "/home/user/video_analysis.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON.")

    assert "frame_number" in data, "Missing 'frame_number' in video_analysis.json"
    assert "leak_address" in data, "Missing 'leak_address' in video_analysis.json"

    # Allow +/- 1 for 0-indexed vs 1-indexed frame numbers
    assert data["frame_number"] in [186, 187, 188], f"Incorrect frame_number: {data['frame_number']}"
    assert data["leak_address"].lower() == "0xc00008e000", f"Incorrect leak_address: {data['leak_address']}"

def test_detector_adversarial_corpus():
    """Verify detector.py against the hidden adversarial corpus."""
    detector_path = "/home/user/detector.py"
    assert os.path.exists(detector_path), f"Detector script {detector_path} does not exist."

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} not found."
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} not found."

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for evil_file in evil_files:
        result = subprocess.run(
            [sys.executable, detector_path, evil_file],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "MALICIOUS":
            evil_bypassed.append(os.path.basename(evil_file))

    # Test clean corpus
    for clean_file in clean_files:
        result = subprocess.run(
            [sys.executable, detector_path, clean_file],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "BENIGN":
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (false positives): {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))