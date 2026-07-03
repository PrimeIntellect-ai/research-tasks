# test_final_state.py

import os
import glob
import subprocess
import pytest

BINARY_PATH = "/home/user/detector/target/release/detector"
VIDEO_PATH = "/app/topology_scan.mp4"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def test_adversarial_corpus():
    assert os.path.isfile(BINARY_PATH), "Binary not found"

    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))

    assert len(evil_files) > 0, "No evil corpus files found"
    assert len(clean_files) > 0, "No clean corpus files found"

    evil_bypassed = []
    clean_modified = []

    for filepath in evil_files:
        cmd = [BINARY_PATH, "--video", VIDEO_PATH, "--log", filepath]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            output = result.stdout.strip()
            if output != "REJECT":
                evil_bypassed.append((os.path.basename(filepath), output))
        except Exception as e:
            evil_bypassed.append((os.path.basename(filepath), str(e)))

    for filepath in clean_files:
        cmd = [BINARY_PATH, "--video", VIDEO_PATH, "--log", filepath]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            output = result.stdout.strip()
            if output != "ACCEPT":
                clean_modified.append((os.path.basename(filepath), output))
        except Exception as e:
            clean_modified.append((os.path.basename(filepath), str(e)))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: " + ", ".join([f"{f} (got {o})" for f, o in evil_bypassed]))
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: " + ", ".join([f"{f} (got {o})" for f, o in clean_modified]))

    if error_msgs:
        pytest.fail("\n".join(error_msgs))