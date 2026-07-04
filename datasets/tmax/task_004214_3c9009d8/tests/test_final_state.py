# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_PATH = "/app/detector"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_PATH), f"Detector binary not found at {DETECTOR_PATH}"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector binary at {DETECTOR_PATH} is not executable"

def test_detector_against_corpora():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    failed_clean = []
    for clean_file in clean_files:
        result = subprocess.run([DETECTOR_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(clean_file))

    failed_evil = []
    for evil_file in evil_files:
        result = subprocess.run([DETECTOR_PATH, evil_file], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(evil_file))

    error_messages = []
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected (expected exit code 0). Offending files: {', '.join(failed_clean[:10])}{'...' if len(failed_clean) > 10 else ''}")
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed (expected exit code 1). Offending files: {', '.join(failed_evil[:10])}{'...' if len(failed_evil) > 10 else ''}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))