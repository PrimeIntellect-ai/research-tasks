# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_task1_corrupted_frames():
    """Check if the corrupted_frames.txt contains the correct frame numbers."""
    target_file = "/home/user/corrupted_frames.txt"
    assert os.path.isfile(target_file), f"Missing {target_file}"

    with open(target_file, "r") as f:
        content = f.read().strip().splitlines()

    expected = ["14", "27", "41"]
    assert content == expected, f"Expected {expected}, but got {content} in {target_file}"

def test_task2_sanitizer_executable():
    """Check if the sanitizer executable exists and is executable."""
    executable_path = "/home/user/sanitizer"
    assert os.path.isfile(executable_path), f"Missing executable at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"

def test_task2_sanitizer_adversarial_corpus():
    """Run the sanitizer against the clean and evil corpora."""
    executable_path = "/home/user/sanitizer"
    assert os.path.isfile(executable_path), f"Missing executable at {executable_path}"

    clean_dir = "/app/adversarial/clean"
    evil_dir = "/app/adversarial/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failures = []
    for f in clean_files:
        result = subprocess.run([executable_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run([executable_path, f], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))