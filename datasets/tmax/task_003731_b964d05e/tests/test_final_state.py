# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_PATH = "/home/user/detector"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"
EVIL_CORPUS_DIR = "/app/corpora/evil/"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_PATH), f"Detector script is missing: {DETECTOR_PATH}"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector script is not executable: {DETECTOR_PATH}"

def test_adversarial_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    assert len(clean_files) > 0, "No clean files found to test."
    assert len(evil_files) > 0, "No evil files found to test."

    failed_clean = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(filepath, 'r') as f:
            payload = f.read().strip()

        result = subprocess.run([DETECTOR_PATH, payload], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(filename)

    failed_evil = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        with open(filepath, 'r') as f:
            payload = f.read().strip()

        result = subprocess.run([DETECTOR_PATH, payload], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(filename)

    error_messages = []
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_clean)}")
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_evil)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))