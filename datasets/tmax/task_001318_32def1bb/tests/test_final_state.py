# test_final_state.py

import os
import subprocess
import pytest

FILTER_BIN = "/home/user/filter"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_filter_binary_exists():
    assert os.path.isfile(FILTER_BIN), f"The filter binary was not found at {FILTER_BIN}"
    assert os.access(FILTER_BIN, os.X_OK), f"The filter binary at {FILTER_BIN} is not executable"

def test_filter_against_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in the evil corpus directory."

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run([FILTER_BIN, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed (expected exit code 1). Offending files: {', '.join(bypassed_files)}")

def test_filter_against_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in the clean corpus directory."

    modified_files = []
    for filepath in clean_files:
        result = subprocess.run([FILTER_BIN, filepath], capture_output=True)
        if result.returncode != 0:
            modified_files.append(os.path.basename(filepath))

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified/rejected (expected exit code 0). Offending files: {', '.join(modified_files)}")