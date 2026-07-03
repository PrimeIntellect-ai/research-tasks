# test_final_state.py

import os
import glob
import subprocess
import pytest

EXECUTABLE_PATH = "/home/user/spectro_filter/target/release/spectro_filter"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_executable_exists():
    """Ensure the Rust binary has been compiled and exists in the expected location."""
    assert os.path.exists(EXECUTABLE_PATH), f"Executable not found at {EXECUTABLE_PATH}. Did you compile it in release mode?"
    assert os.path.isfile(EXECUTABLE_PATH), f"{EXECUTABLE_PATH} is not a file."
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"{EXECUTABLE_PATH} is not executable."

def test_adversarial_corpus():
    """
    Test the executable against the clean and evil corpora.
    Clean files must exit with 0.
    Evil files must exit with non-zero.
    """
    assert os.path.exists(EXECUTABLE_PATH), "Executable missing."

    clean_files = sorted(glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv")))
    evil_files = sorted(glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv")))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failures = []
    for f in clean_files:
        result = subprocess.run([EXECUTABLE_PATH, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run([EXECUTABLE_PATH, f], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))