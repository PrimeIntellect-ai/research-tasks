# test_final_state.py

import os
import subprocess
import glob
import pytest

DETECTOR_PATH = "/home/user/detector"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_PATH), f"Detector executable not found at {DETECTOR_PATH}"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector at {DETECTOR_PATH} is not executable"

def test_adversarial_corpus_evil():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*"))
    assert len(evil_files) > 0, f"No files found in evil corpus directory {EVIL_CORPUS_DIR}"

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run([DETECTOR_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed_files)}")

def test_adversarial_corpus_clean():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*"))
    assert len(clean_files) > 0, f"No files found in clean corpus directory {CLEAN_CORPUS_DIR}"

    modified_files = []
    for filepath in clean_files:
        result = subprocess.run([DETECTOR_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            modified_files.append(os.path.basename(filepath))

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified/flagged. Offending files: {', '.join(modified_files)}")