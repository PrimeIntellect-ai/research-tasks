# test_final_state.py
import os
import subprocess
import pytest

def test_detector_exists_and_executable():
    detector_path = "/home/user/detector.sh"
    assert os.path.isfile(detector_path), f"Detector script missing: {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector script is not executable: {detector_path}"

def test_adversarial_corpus():
    detector_path = "/home/user/detector.sh"
    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    evil_failed = []

    # Test clean corpus
    for cf in clean_files:
        result = subprocess.run([detector_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    # Test evil corpus
    for ef in evil_files:
        result = subprocess.run([detector_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    assert not error_messages, " | ".join(error_messages)