# test_final_state.py

import os
import glob
import subprocess
import pytest

BINARY_PATH = "/home/user/validator"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

def test_binary_exists_and_executable():
    """Check if the compiled binary exists and is executable."""
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}. Did you compile your C program?"
    assert os.access(BINARY_PATH, os.X_OK), f"File at {BINARY_PATH} is not executable."

def test_clean_corpus_accepted():
    """Ensure all clean CSV files exit with status code 0."""
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.csv"))
    assert clean_files, f"No CSV files found in {CLEAN_DIR}."

    rejected_files = []
    for filepath in clean_files:
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            rejected_files.append(os.path.basename(filepath))

    assert not rejected_files, (
        f"{len(rejected_files)} of {len(clean_files)} clean files were incorrectly rejected "
        f"(expected exit code 0): {', '.join(rejected_files)}"
    )

def test_evil_corpus_rejected():
    """Ensure all evil/corrupted CSV files exit with status code 1."""
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.csv"))
    assert evil_files, f"No CSV files found in {EVIL_DIR}."

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(filepath))

    assert not bypassed_files, (
        f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed the validator "
        f"(expected exit code 1): {', '.join(bypassed_files)}"
    )