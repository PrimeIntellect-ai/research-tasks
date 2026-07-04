# test_final_state.py
import os
import subprocess
import pytest

def test_detector_exists_and_executable():
    detector_path = "/home/user/detector"
    assert os.path.exists(detector_path), f"Detector binary {detector_path} does not exist. Did you compile it?"
    assert os.path.isfile(detector_path), f"{detector_path} is not a file."
    assert os.access(detector_path, os.X_OK), f"Detector binary {detector_path} is not executable."

def test_adversarial_corpus():
    detector_path = "/home/user/detector"
    evil_dir = "/corpus/evil/"
    clean_dir = "/corpus/clean/"

    evil_bypassed = []
    clean_rejected = []

    # Test evil corpus
    assert os.path.exists(evil_dir), f"Evil corpus directory {evil_dir} does not exist."
    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read().strip()
        result = subprocess.run([detector_path, content], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(filename)

    # Test clean corpus
    assert os.path.exists(clean_dir), f"Clean corpus directory {clean_dir} does not exist."
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read().strip()
        result = subprocess.run([detector_path, content], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(filename)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_msgs.append(f"{len(clean_rejected)} of {len(clean_files)} clean rejected: {', '.join(clean_rejected)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))