# test_final_state.py

import os
import glob
import subprocess
import pytest

FILTER_BIN = "/home/user/secure_filter"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_secure_filter_exists_and_executable():
    assert os.path.exists(FILTER_BIN), f"The executable {FILTER_BIN} does not exist. Did you compile your C++ program?"
    assert os.path.isfile(FILTER_BIN), f"{FILTER_BIN} is not a file."
    assert os.access(FILTER_BIN, os.X_OK), f"{FILTER_BIN} is not executable."

def run_filter(file_path):
    result = subprocess.run(
        [FILTER_BIN, file_path],
        capture_output=True,
        text=True,
        timeout=2
    )
    return result.stdout.strip()

def test_clean_corpus_accepted():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*"))
    assert len(clean_files) > 0, f"No files found in {CLEAN_CORPUS_DIR}"

    rejected_files = []

    for file_path in clean_files:
        output = run_filter(file_path)
        if output != "ACCEPT":
            rejected_files.append((os.path.basename(file_path), output))

    if rejected_files:
        details = ", ".join([f"{f} (output: {o!r})" for f, o in rejected_files[:5]])
        pytest.fail(f"{len(rejected_files)} of {len(clean_files)} clean files were rejected (or had invalid output). Examples: {details}")

def test_evil_corpus_rejected():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*"))
    assert len(evil_files) > 0, f"No files found in {EVIL_CORPUS_DIR}"

    accepted_files = []

    for file_path in evil_files:
        output = run_filter(file_path)
        if output != "REJECT":
            accepted_files.append((os.path.basename(file_path), output))

    if accepted_files:
        details = ", ".join([f"{f} (output: {o!r})" for f, o in accepted_files[:5]])
        pytest.fail(f"{len(accepted_files)} of {len(evil_files)} evil files bypassed the filter (or had invalid output). Examples: {details}")