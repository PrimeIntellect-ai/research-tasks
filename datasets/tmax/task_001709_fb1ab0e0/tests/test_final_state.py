# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_SCRIPT = "/home/user/detector.sh"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"
EVIL_CORPUS_DIR = "/app/corpora/evil/"

def test_detector_script_exists_and_executable():
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"
    assert os.access(DETECTOR_SCRIPT, os.X_OK), f"Detector script at {DETECTOR_SCRIPT} is not executable"

def test_detector_on_corpora():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.wav')]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.wav')]

    assert len(clean_files) > 0, "No clean files found to test."
    assert len(evil_files) > 0, "No evil files found to test."

    clean_failed = []
    for clean_file in clean_files:
        result = subprocess.run([DETECTOR_SCRIPT, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(clean_file))

    evil_failed = []
    for evil_file in evil_files:
        result = subprocess.run([DETECTOR_SCRIPT, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(evil_file))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed[:5])}{'...' if len(clean_failed) > 5 else ''}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed[:5])}{'...' if len(evil_failed) > 5 else ''}")

    assert not errors, " | ".join(errors)