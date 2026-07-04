# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_detector_exists_and_executable():
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector executable not found at {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector at {detector_path} is not executable"

def test_adversarial_corpus():
    detector_path = "/home/user/detector"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.wav"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.wav"))

    assert len(clean_files) > 0, f"No files found in {clean_dir}"
    assert len(evil_files) > 0, f"No files found in {evil_dir}"

    clean_failed = []
    for f in clean_files:
        result = subprocess.run([detector_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        result = subprocess.run([detector_path, f], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(f))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

    assert not error_messages, "\n".join(error_messages)