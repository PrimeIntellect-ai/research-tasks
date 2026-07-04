# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_SCRIPT = "/home/user/detector.py"
CLEAN_CORPUS_DIR = "/app/test_clean"
EVIL_CORPUS_DIR = "/app/test_evil"

def test_detector_exists():
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"

def run_detector(filepath):
    result = subprocess.run(
        ["python3", DETECTOR_SCRIPT, filepath],
        capture_output=True,
        text=True,
        timeout=10
    )
    return result.stdout.strip()

def test_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.txt')]
    assert len(clean_files) > 0, "No clean files found to test."

    failures = []
    for filepath in clean_files:
        output = run_detector(filepath)
        if output != "CLEAN":
            failures.append(os.path.basename(filepath))

    if failures:
        pytest.fail(f"{len(failures)} of {len(clean_files)} clean files modified/rejected (expected CLEAN). Offending files: {failures}")

def test_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.txt')]
    assert len(evil_files) > 0, "No evil files found to test."

    failures = []
    for filepath in evil_files:
        output = run_detector(filepath)
        if output != "EVIL":
            failures.append(os.path.basename(filepath))

    if failures:
        pytest.fail(f"{len(failures)} of {len(evil_files)} evil files bypassed (expected EVIL). Offending files: {failures}")