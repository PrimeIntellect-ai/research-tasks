# test_final_state.py

import os
import subprocess
import pytest

def test_detector_script_exists_and_executable():
    detector_path = "/home/user/detector.sh"
    assert os.path.exists(detector_path), f"Detector script {detector_path} does not exist."
    assert os.access(detector_path, os.X_OK), f"Detector script {detector_path} is not executable."

def test_threshold_file():
    threshold_path = "/home/user/threshold.txt"
    assert os.path.exists(threshold_path), f"Threshold file {threshold_path} does not exist."
    with open(threshold_path, "r") as f:
        content = f.read().strip()
    assert content.isdigit(), f"Threshold file must contain a single integer, found: {content}"

def test_adversarial_corpus():
    detector_path = "/home/user/detector.sh"
    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_rejected = 0
    evil_bypassed = []
    for fpath in evil_files:
        result = subprocess.run([detector_path, fpath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 1:
            evil_rejected += 1
        else:
            evil_bypassed.append(os.path.basename(fpath))

    clean_preserved = 0
    clean_modified = []
    for fpath in clean_files:
        result = subprocess.run([detector_path, fpath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            clean_preserved += 1
        else:
            clean_modified.append(os.path.basename(fpath))

    evil_success_rate = evil_rejected / len(evil_files) if evil_files else 0
    clean_success_rate = clean_preserved / len(clean_files) if clean_files else 0

    errors = []
    if evil_success_rate < 0.95:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (expected <= 5%). Examples: {evil_bypassed[:5]}")
    if clean_success_rate < 0.95:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected (expected <= 5%). Examples: {clean_modified[:5]}")

    assert not errors, "\n".join(errors)