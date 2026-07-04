# test_final_state.py

import os
import subprocess
import pytest

def test_downtime_frames():
    """Test that the downtime frames are correctly identified and written."""
    path = "/home/user/downtime_frames.txt"
    assert os.path.exists(path), f"File {path} does not exist. You must create it with the downtime frame indices."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_frames = ["150", "151", "152", "153", "154", "155"]
    assert lines == expected_frames, f"Expected frames {expected_frames}, but got {lines} in {path}"

def test_detector_script():
    """Test that the detector script correctly classifies clean and evil files."""
    script_path = "/home/user/detector.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    clean_dir = "/app/telemetry_corpus/clean/"
    evil_dir = "/app/telemetry_corpus/evil/"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_modified = []
    for cf in clean_files:
        res = subprocess.run(["/bin/bash", script_path, cf])
        if res.returncode != 0:
            clean_modified.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        res = subprocess.run(["/bin/bash", script_path, ef])
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))