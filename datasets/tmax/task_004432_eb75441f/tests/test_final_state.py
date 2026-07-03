# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/evaluate_benchmarks.py"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"
EVIL_CORPUS_DIR = "/app/corpora/evil/"

def test_script_exists():
    """Check if the user script exists."""
    assert os.path.isfile(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"

def test_clean_corpus():
    """Check that all clean files return exit code 0."""
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    assert len(clean_files) > 0, f"No clean files found in {CLEAN_CORPUS_DIR}"

    failed_files = []
    for csv_file in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, csv_file], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(csv_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files failed (expected exit code 0): {failed_files}")

def test_evil_corpus():
    """Check that all evil files return exit code 1."""
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))
    assert len(evil_files) > 0, f"No evil files found in {EVIL_CORPUS_DIR}"

    failed_files = []
    for csv_file in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, csv_file], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(csv_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected exit code 1): {failed_files}")