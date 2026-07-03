# test_final_state.py

import os
import glob
import subprocess
import pytest

EXECUTABLE_PATH = "/home/user/deadlock_detector"
CLEAN_CORPUS_DIR = "/home/user/corpora/clean"
EVIL_CORPUS_DIR = "/home/user/corpora/evil"

def test_executable_exists_and_is_executable():
    assert os.path.isfile(EXECUTABLE_PATH), f"Executable not found at {EXECUTABLE_PATH}"
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"File at {EXECUTABLE_PATH} is not executable"

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    assert len(clean_files) > 0, f"No clean CSV files found in {CLEAN_CORPUS_DIR}"

    failed_files = []
    for csv_file in clean_files:
        result = subprocess.run([EXECUTABLE_PATH, csv_file], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(csv_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (expected exit code 0): {', '.join(failed_files)}")

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))
    assert len(evil_files) > 0, f"No evil CSV files found in {EVIL_CORPUS_DIR}"

    failed_files = []
    for csv_file in evil_files:
        result = subprocess.run([EXECUTABLE_PATH, csv_file], capture_output=True)
        # The prompt says: "If ANY cycle is found (deadlock), the program must exit with status code 1"
        # and "strictly non-zero" in pass criterion.
        if result.returncode == 0:
            failed_files.append(os.path.basename(csv_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (expected non-zero exit code): {', '.join(failed_files)}")