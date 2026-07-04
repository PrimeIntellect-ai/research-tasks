# test_final_state.py

import os
import subprocess
import pytest

CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"
ENTRY_POINT = "/home/user/classifier/target/release/classifier"

def test_classifier_exists():
    assert os.path.exists(ENTRY_POINT), f"Classifier binary not found at {ENTRY_POINT}"
    assert os.path.isfile(ENTRY_POINT), f"{ENTRY_POINT} is not a file"
    assert os.access(ENTRY_POINT, os.X_OK), f"Classifier binary at {ENTRY_POINT} is not executable"

def test_adversarial_corpus():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus missing or not a directory at {CLEAN_DIR}"
    assert os.path.isdir(EVIL_DIR), f"Evil corpus missing or not a directory at {EVIL_DIR}"

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith('.astro')]
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith('.astro')]

    assert len(clean_files) > 0, "No clean files found in corpus"
    assert len(evil_files) > 0, "No evil files found in corpus"

    clean_failures = []
    for f in clean_files:
        res = subprocess.run([ENTRY_POINT, f], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        res = subprocess.run([ENTRY_POINT, f], capture_output=True)
        if res.returncode == 0:
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))