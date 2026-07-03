# test_final_state.py
import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sanitizer.py"
CLEAN_DIR = "/app/corpora/clean/"
EVIL_DIR = "/app/corpora/evil/"

def test_sanitizer_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Sanitizer script not found at {SCRIPT_PATH}"

def test_adversarial_corpus():
    assert os.path.isfile(SCRIPT_PATH), f"Sanitizer script not found at {SCRIPT_PATH}"

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_DIR}."
    assert len(evil_files) > 0, f"No evil files found in {EVIL_DIR}."

    clean_failures = []
    evil_failures = []

    for f in clean_files:
        res = subprocess.run(["python3", SCRIPT_PATH, f], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(f))

    for f in evil_files:
        res = subprocess.run(["python3", SCRIPT_PATH, f], capture_output=True)
        if res.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified or rejected: {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))