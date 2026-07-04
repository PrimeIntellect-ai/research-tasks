# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_PATH = "/home/user/detector"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_detector_exists_and_executable():
    assert os.path.exists(DETECTOR_PATH), f"Detector script not found at {DETECTOR_PATH}"
    assert os.path.isfile(DETECTOR_PATH), f"{DETECTOR_PATH} is not a file"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector script at {DETECTOR_PATH} is not executable"

def test_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, f"No files found in clean corpus: {CLEAN_CORPUS_DIR}"

    failed_clean = []

    for filepath in clean_files:
        result = subprocess.run([DETECTOR_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(filepath))

    if failed_clean:
        pytest.fail(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_clean)}")

def test_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, f"No files found in evil corpus: {EVIL_CORPUS_DIR}"

    failed_evil = []

    for filepath in evil_files:
        result = subprocess.run([DETECTOR_PATH, filepath], capture_output=True)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(filepath))

    if failed_evil:
        pytest.fail(f"{len(failed_evil)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_evil)}")