# test_final_state.py

import os
import subprocess
import pytest
import glob

def test_parseman_built():
    assert os.path.isfile("/app/parseman-1.0/parseman"), "parseman executable was not built in /app/parseman-1.0"
    assert os.access("/app/parseman-1.0/parseman", os.X_OK), "/app/parseman-1.0/parseman is not executable"

def test_detector_exists():
    assert os.path.isfile("/home/user/detector.c"), "/home/user/detector.c source file is missing"
    assert os.path.isfile("/home/user/detector"), "/home/user/detector executable is missing"
    assert os.access("/home/user/detector", os.X_OK), "/home/user/detector is not executable"

def test_adversarial_corpus():
    detector_path = "/home/user/detector"

    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*"))
    clean_files = glob.glob(os.path.join(clean_dir, "*"))

    assert len(evil_files) > 0, "No evil files found in corpus."
    assert len(clean_files) > 0, "No clean files found in corpus."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run([detector_path, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run([detector_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))