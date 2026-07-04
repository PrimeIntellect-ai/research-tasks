# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_BIN = "/home/user/detector"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_detector_exists_and_executable():
    assert os.path.exists(DETECTOR_BIN), f"Missing detector binary: {DETECTOR_BIN}"
    assert os.path.isfile(DETECTOR_BIN), f"Not a file: {DETECTOR_BIN}"
    assert os.access(DETECTOR_BIN, os.X_OK), f"Detector binary is not executable: {DETECTOR_BIN}"

def test_clean_corpus():
    if not os.path.exists(DETECTOR_BIN) or not os.access(DETECTOR_BIN, os.X_OK):
        pytest.skip("Detector binary missing or not executable")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, f"No files found in {CLEAN_CORPUS_DIR}"

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run([DETECTOR_BIN, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected (expected exit code 0). "
                    f"Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    if not os.path.exists(DETECTOR_BIN) or not os.access(DETECTOR_BIN, os.X_OK):
        pytest.skip("Detector binary missing or not executable")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, f"No files found in {EVIL_CORPUS_DIR}"

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run([DETECTOR_BIN, filepath], capture_output=True)
        if result.returncode == 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected exit code non-zero, e.g., 1). "
                    f"Offending files: {', '.join(failed_files)}")