# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/detect.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_detect_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Detector script missing: {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Detector script is not executable: {SCRIPT_PATH}"

def test_clean_corpus_accepted():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.c"))
    assert len(clean_files) > 0, "No clean corpus files found to test."

    rejected = []
    for c_file in clean_files:
        result = subprocess.run([SCRIPT_PATH, c_file], capture_output=True)
        if result.returncode != 0:
            rejected.append(os.path.basename(c_file))

    if rejected:
        pytest.fail(f"{len(rejected)} of {len(clean_files)} clean rejected: {', '.join(rejected)}")

def test_evil_corpus_rejected():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.c"))
    assert len(evil_files) > 0, "No evil corpus files found to test."

    bypassed = []
    for c_file in evil_files:
        result = subprocess.run([SCRIPT_PATH, c_file], capture_output=True)
        if result.returncode == 0:
            bypassed.append(os.path.basename(c_file))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")