# test_final_state.py

import os
import subprocess
import pytest

FILTER_BIN = "/home/user/filter"
CLEAN_DIR = "/home/user/validation/clean"
EVIL_DIR = "/home/user/validation/evil"

def test_filter_binary_exists():
    assert os.path.exists(FILTER_BIN), f"Filter binary not found at {FILTER_BIN}"
    assert os.path.isfile(FILTER_BIN), f"{FILTER_BIN} is not a file"
    assert os.access(FILTER_BIN, os.X_OK), f"{FILTER_BIN} is not executable"

def test_filter_clean_corpus():
    if not os.path.exists(FILTER_BIN) or not os.access(FILTER_BIN, os.X_OK):
        pytest.fail("Executable filter not found.")

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert clean_files, f"No clean files found in {CLEAN_DIR}"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([FILTER_BIN, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")

def test_filter_evil_corpus():
    if not os.path.exists(FILTER_BIN) or not os.access(FILTER_BIN, os.X_OK):
        pytest.fail("Executable filter not found.")

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert evil_files, f"No evil files found in {EVIL_DIR}"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([FILTER_BIN, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_files)}")