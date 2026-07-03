# test_final_state.py

import os
import glob
import subprocess
import pytest

EXECUTABLE = "/home/user/run_filter"
EVIL_DIR = "/app/eval_data/evil/"
CLEAN_DIR = "/app/eval_data/clean/"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} does not exist. Did you compile your C program?"
    assert os.access(EXECUTABLE, os.X_OK), f"File {EXECUTABLE} is not executable."

def test_adversarial_corpus():
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.csv"))
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.csv"))

    assert len(evil_files) > 0, f"No evil files found in {EVIL_DIR}."
    assert len(clean_files) > 0, f"No clean files found in {CLEAN_DIR}."

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for f in evil_files:
        try:
            result = subprocess.run([EXECUTABLE, f], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "REJECT":
                evil_bypassed.append(os.path.basename(f))
        except Exception:
            evil_bypassed.append(os.path.basename(f))

    # Test clean corpus
    for f in clean_files:
        try:
            result = subprocess.run([EXECUTABLE, f], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "ACCEPT":
                clean_modified.append(os.path.basename(f))
        except Exception:
            clean_modified.append(os.path.basename(f))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))