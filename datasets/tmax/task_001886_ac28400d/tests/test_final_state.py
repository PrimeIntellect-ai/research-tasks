# test_final_state.py
import os
import subprocess
import pytest

DETECTOR_PATH = "/home/user/detector"
EVIL_CORPUS_DIR = "/home/user/corpus/evil/"
CLEAN_CORPUS_DIR = "/home/user/corpus/clean/"

def test_detector_exists_and_executable():
    assert os.path.exists(DETECTOR_PATH), f"Detector executable not found at {DETECTOR_PATH}"
    assert os.path.isfile(DETECTOR_PATH), f"{DETECTOR_PATH} is not a file"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector at {DETECTOR_PATH} is not executable"

def test_detector_accuracy():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Missing evil corpus directory: {EVIL_CORPUS_DIR}"
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Missing clean corpus directory: {CLEAN_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    clean_modified = []

    for filepath in evil_files:
        result = subprocess.run([DETECTOR_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(filepath))

    for filepath in clean_files:
        result = subprocess.run([DETECTOR_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(filepath))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))