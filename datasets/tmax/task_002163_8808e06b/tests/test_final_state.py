# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_PATH = "/home/user/detector"
EVIL_CORPUS_DIR = "/app/hidden_corpus/evil/"
CLEAN_CORPUS_DIR = "/app/hidden_corpus/clean/"

def test_detector_exists_and_executable():
    """Verify that the compiled detector binary exists and is executable."""
    assert os.path.isfile(DETECTOR_PATH), f"Detector binary not found at {DETECTOR_PATH}"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector binary at {DETECTOR_PATH} is not executable"

def test_evil_corpus_rejection():
    """Verify that all files in the evil corpus are rejected correctly."""
    if not os.path.isfile(DETECTOR_PATH):
        pytest.skip("Detector binary not found")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, f"No files found in {EVIL_CORPUS_DIR}"

    bypassed = []

    for filename in evil_files:
        file_path = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run([DETECTOR_PATH, file_path], capture_output=True, text=True)

        stdout_clean = result.stdout.strip()
        if result.returncode != 1 or stdout_clean != "EVIL":
            bypassed.append(filename)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {bypassed}")

def test_clean_corpus_acceptance():
    """Verify that all files in the clean corpus are accepted correctly."""
    if not os.path.isfile(DETECTOR_PATH):
        pytest.skip("Detector binary not found")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, f"No files found in {CLEAN_CORPUS_DIR}"

    modified = []

    for filename in clean_files:
        file_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run([DETECTOR_PATH, file_path], capture_output=True, text=True)

        stdout_clean = result.stdout.strip()
        if result.returncode != 0 or stdout_clean != "CLEAN":
            modified.append(filename)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (incorrectly flagged). Offending files: {modified}")