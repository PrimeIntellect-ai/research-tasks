# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_PATH = "/home/user/detector"
EVIL_DIR = "/app/evil"
CLEAN_DIR = "/app/clean"

def test_detector_exists():
    assert os.path.isfile(DETECTOR_PATH), f"Executable not found at {DETECTOR_PATH}"
    assert os.access(DETECTOR_PATH, os.X_OK), f"File at {DETECTOR_PATH} is not executable"

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.txt')]
    assert len(evil_files) > 0, f"No text files found in {EVIL_DIR}"

    bypassed = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        result = subprocess.run([DETECTOR_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed.append(filename)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed (expected exit code 1). Offending files: {', '.join(bypassed[:10])}")

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.txt')]
    assert len(clean_files) > 0, f"No text files found in {CLEAN_DIR}"

    modified = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        result = subprocess.run([DETECTOR_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            modified.append(filename)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/rejected (expected exit code 0). Offending files: {', '.join(modified[:10])}")