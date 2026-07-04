# test_final_state.py

import os
import subprocess
import glob
import pytest

DETECTOR_PATH = "/home/user/detector"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_detector_exists_and_executable():
    assert os.path.exists(DETECTOR_PATH), f"Detector binary not found at {DETECTOR_PATH}"
    assert os.path.isfile(DETECTOR_PATH), f"Detector path {DETECTOR_PATH} is not a file"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector binary at {DETECTOR_PATH} is not executable"

def test_detector_against_corpora():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*"))

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_CORPUS_DIR}"
    assert len(evil_files) > 0, f"No evil files found in {EVIL_CORPUS_DIR}"

    clean_failures = []
    for f in clean_files:
        result = subprocess.run([DETECTOR_PATH, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run([DETECTOR_PATH, f], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))