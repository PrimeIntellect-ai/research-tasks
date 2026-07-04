# test_final_state.py

import os
import subprocess
import pytest

EXECUTABLE = "/home/user/dataset_filter"
EVIL_DIR = "/app/datasets/evil/"
CLEAN_DIR = "/app/datasets/clean/"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory missing: {EVIL_DIR}"
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing: {CLEAN_DIR}"

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith('.tar')]
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith('.tar')]

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    for evil_file in evil_files:
        with open(evil_file, 'rb') as f:
            result = subprocess.run([EXECUTABLE], stdin=f, capture_output=True)
            if result.returncode != 1:
                evil_bypassed.append(os.path.basename(evil_file))

    for clean_file in clean_files:
        with open(clean_file, 'rb') as f:
            result = subprocess.run([EXECUTABLE], stdin=f, capture_output=True)
            if result.returncode != 0:
                clean_modified.append(os.path.basename(clean_file))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not error_msg, " | ".join(error_msg)