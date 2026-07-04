# test_final_state.py

import os
import subprocess
import pytest

EXECUTABLE_PATH = "/home/user/trace_filter"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_executable_exists_and_is_file():
    assert os.path.exists(EXECUTABLE_PATH), f"Executable {EXECUTABLE_PATH} does not exist."
    assert os.path.isfile(EXECUTABLE_PATH), f"{EXECUTABLE_PATH} is not a file."
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"{EXECUTABLE_PATH} is not executable."

def test_clean_corpus_accepted():
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    assert len(clean_files) > 0, f"No CSV files found in {CLEAN_CORPUS_DIR}."

    rejected_files = []
    for f in clean_files:
        result = subprocess.run([EXECUTABLE_PATH, f], capture_output=True)
        if result.returncode != 0:
            rejected_files.append(os.path.basename(f))

    if rejected_files:
        pytest.fail(f"{len(rejected_files)} of {len(clean_files)} clean rejected: {', '.join(rejected_files)}")

def test_evil_corpus_rejected():
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]
    assert len(evil_files) > 0, f"No CSV files found in {EVIL_CORPUS_DIR}."

    bypassed_files = []
    for f in evil_files:
        result = subprocess.run([EXECUTABLE_PATH, f], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(f))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")