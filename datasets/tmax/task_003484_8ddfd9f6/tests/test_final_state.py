# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_detector_exists_and_executable():
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector executable not found at {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector at {detector_path} is not executable"

def test_detector_clean_corpus():
    detector_path = "/home/user/detector"
    clean_files = glob.glob("/app/corpora/clean/*.fasta")
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([detector_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected (expected exit code 0). Offending files: {', '.join(failed_files)}")

def test_detector_evil_corpus():
    detector_path = "/home/user/detector"
    evil_files = glob.glob("/app/corpora/evil/*.fasta")
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([detector_path, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (expected exit code 1). Offending files: {', '.join(failed_files)}")