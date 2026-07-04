# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_PATH = "/home/user/detector"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_detector_exists_and_executable():
    """Verify that the detector script exists and is executable."""
    assert os.path.isfile(DETECTOR_PATH), f"Detector script not found at {DETECTOR_PATH}"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector script at {DETECTOR_PATH} is not executable"

def test_evil_corpus_rejected():
    """Verify that all files in the evil corpus are rejected (exit code 1)."""
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.fail(f"Evil corpus directory missing: {EVIL_CORPUS_DIR}")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, f"No files found in {EVIL_CORPUS_DIR}"

    bypassed = []
    for filename in evil_files:
        file_path = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run([DETECTOR_PATH, file_path], capture_output=True)
        if result.returncode != 1:
            bypassed.append(filename)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed (did not exit with code 1). Offending files: {', '.join(bypassed)}")

def test_clean_corpus_accepted():
    """Verify that all files in the clean corpus are accepted (exit code 0)."""
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.fail(f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, f"No files found in {CLEAN_CORPUS_DIR}"

    rejected = []
    for filename in clean_files:
        file_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run([DETECTOR_PATH, file_path], capture_output=True)
        if result.returncode != 0:
            rejected.append(filename)

    if rejected:
        pytest.fail(f"{len(rejected)} of {len(clean_files)} clean modified/rejected (did not exit with code 0). Offending files: {', '.join(rejected)}")