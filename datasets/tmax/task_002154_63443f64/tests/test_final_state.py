# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_PATH = "/home/user/detector"
EVIL_CORPUS_PATH = "/app/corpus/evil/"
CLEAN_CORPUS_PATH = "/app/corpus/clean/"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_PATH), f"Detector binary missing: {DETECTOR_PATH} should exist."
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector binary is not executable: {DETECTOR_PATH}"

def test_detector_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS_PATH), f"Evil corpus directory missing: {EVIL_CORPUS_PATH}"

    evil_files = [f for f in os.listdir(EVIL_CORPUS_PATH) if os.path.isfile(os.path.join(EVIL_CORPUS_PATH, f))]
    assert len(evil_files) > 0, f"Evil corpus directory {EVIL_CORPUS_PATH} is empty."

    bypassed = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_PATH, filename)
        result = subprocess.run([DETECTOR_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed.append(filename)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed (expected exit code 1). Offending files: {', '.join(bypassed)}")

def test_detector_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS_PATH), f"Clean corpus directory missing: {CLEAN_CORPUS_PATH}"

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_PATH) if os.path.isfile(os.path.join(CLEAN_CORPUS_PATH, f))]
    assert len(clean_files) > 0, f"Clean corpus directory {CLEAN_CORPUS_PATH} is empty."

    modified = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_PATH, filename)
        result = subprocess.run([DETECTOR_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            modified.append(filename)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/rejected (expected exit code 0). Offending files: {', '.join(modified)}")