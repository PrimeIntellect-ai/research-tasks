# test_final_state.py

import os
import subprocess
import pytest

def test_detector_go_exists():
    path = "/home/user/detector.go"
    assert os.path.isfile(path), f"Missing required file: {path}"

def test_detector_classification():
    detector_path = "/home/user/detector.go"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isfile(detector_path), f"Missing detector program at {detector_path}"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for f in clean_files:
        result = subprocess.run(["go", "run", detector_path, f], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "CLEAN":
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run(["go", "run", detector_path, f], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "EVIL":
            evil_failures.append(os.path.basename(f))

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/flagged. Offending files: {', '.join(clean_failures)}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(evil_failures)}")

    assert not clean_failures and not evil_failures, " | ".join(error_msg)