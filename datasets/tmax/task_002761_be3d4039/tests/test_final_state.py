# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_SCRIPT = "/home/user/detector.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def run_detector(filepath):
    """Run the detector script on a given file and return the exit code."""
    result = subprocess.run(
        ["python3", DETECTOR_SCRIPT, filepath],
        capture_output=True
    )
    return result.returncode

def test_detector_exists():
    assert os.path.isfile(DETECTOR_SCRIPT), f"The detector script is missing at {DETECTOR_SCRIPT}."

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    failed_files = []
    total_files = 0
    for filename in sorted(os.listdir(CLEAN_CORPUS_DIR)):
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        if os.path.isfile(filepath):
            total_files += 1
            code = run_detector(filepath)
            if code != 0:
                failed_files.append(filename)

    assert not failed_files, (
        f"{len(failed_files)} of {total_files} clean files modified/rejected (expected exit code 0). "
        f"Offending files: {failed_files}"
    )

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    failed_files = []
    total_files = 0
    for filename in sorted(os.listdir(EVIL_CORPUS_DIR)):
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        if os.path.isfile(filepath):
            total_files += 1
            code = run_detector(filepath)
            if code == 0:
                failed_files.append(filename)

    assert not failed_files, (
        f"{len(failed_files)} of {total_files} evil files bypassed detection (expected exit code 1). "
        f"Offending files: {failed_files}"
    )