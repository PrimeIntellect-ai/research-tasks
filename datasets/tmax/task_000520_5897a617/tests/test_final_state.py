# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_PATH = "/home/user/detector.py"
CLEAN_CORPUS_DIR = "/verify/corpus/clean/"
EVIL_CORPUS_DIR = "/verify/corpus/evil/"

def test_detector_exists():
    assert os.path.exists(DETECTOR_PATH), f"Detector script not found at {DETECTOR_PATH}"
    assert os.path.isfile(DETECTOR_PATH), f"{DETECTOR_PATH} is not a file"

def run_detector(filepath):
    """Runs the detector script on the given filepath and returns the exit code."""
    result = subprocess.run(
        ["python3", DETECTOR_PATH, filepath],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode

def test_clean_corpus():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, "No JSON files found in clean corpus"

    failed_files = []
    for filepath in clean_files:
        exit_code = run_detector(filepath)
        if exit_code != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, "No JSON files found in evil corpus"

    failed_files = []
    for filepath in evil_files:
        exit_code = run_detector(filepath)
        if exit_code != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_files)}")