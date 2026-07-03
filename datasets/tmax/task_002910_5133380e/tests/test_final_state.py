# test_final_state.py

import os
import subprocess
import pytest

def test_detector_exists_and_executable():
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector executable not found at {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector at {detector_path} is not executable"

def test_csv_exists():
    csv_path = "/home/user/frame_brightness.csv"
    assert os.path.isfile(csv_path), f"CSV file not found at {csv_path}"

def test_adversarial_corpus():
    detector_path = "/home/user/detector"
    csv_path = "/home/user/frame_brightness.csv"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    assert os.path.isfile(detector_path), "Detector missing"
    assert os.path.isfile(csv_path), "CSV missing"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".txt")]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".txt")]

    clean_modified = []
    evil_bypassed = []

    for f in clean_files:
        log_path = os.path.join(clean_dir, f)
        result = subprocess.run([detector_path, log_path, csv_path], capture_output=True, text=True)
        if result.stdout.strip() != "CLEAN":
            clean_modified.append(f)

    for f in evil_files:
        log_path = os.path.join(evil_dir, f)
        result = subprocess.run([detector_path, log_path, csv_path], capture_output=True, text=True)
        if result.stdout.strip() != "EVIL":
            evil_bypassed.append(f)

    errors = []
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected/misclassified): {', '.join(clean_modified)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (accepted/misclassified): {', '.join(evil_bypassed)}")

    assert not errors, " | ".join(errors)