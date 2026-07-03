# test_final_state.py

import os
import glob
import subprocess
import pytest

EXECUTABLE = "/home/user/dataset_scanner"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.tar"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.tar"))

    assert len(clean_files) > 0, "No clean files found to test."
    assert len(evil_files) > 0, "No evil files found to test."

    clean_failed = []
    evil_failed = []

    for cf in clean_files:
        result = subprocess.run([EXECUTABLE, cf], capture_output=True, text=True)
        if result.returncode != 0 or "CLEAN" not in result.stdout:
            clean_failed.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([EXECUTABLE, ef], capture_output=True, text=True)
        if result.returncode != 1 or "MALICIOUS" not in result.stdout:
            evil_failed.append(os.path.basename(ef))

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))