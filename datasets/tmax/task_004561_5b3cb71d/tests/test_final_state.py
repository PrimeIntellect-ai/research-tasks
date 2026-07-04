# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_BIN = '/home/user/detector_bin'
EVIL_CORPUS_DIR = '/app/corpora/evil'
CLEAN_CORPUS_DIR = '/app/corpora/clean'

def test_detector_bin_exists_and_executable():
    assert os.path.isfile(DETECTOR_BIN), f"Executable not found at {DETECTOR_BIN}"
    assert os.access(DETECTOR_BIN, os.X_OK), f"File at {DETECTOR_BIN} is not executable"

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.wav')]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.wav')]

    assert len(evil_files) > 0, "No evil files found to test"
    assert len(clean_files) > 0, "No clean files found to test"

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run([DETECTOR_BIN, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run([DETECTOR_BIN, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))