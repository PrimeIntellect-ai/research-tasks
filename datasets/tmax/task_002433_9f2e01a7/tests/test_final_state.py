# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/filter.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_filter_behavior():
    # Ensure script exists before running tests
    if not os.path.isfile(SCRIPT_PATH) or not os.access(SCRIPT_PATH, os.X_OK):
        pytest.fail("Filter script is missing or not executable.")

    # Collect clean files
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.fasta')]
    assert len(clean_files) > 0, "No clean FASTA files found to test against."

    # Collect evil files
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.fasta')]
    assert len(evil_files) > 0, "No evil FASTA files found to test against."

    clean_failures = []
    for fname in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, fname)
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(fname)

    evil_failures = []
    for fname in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, fname)
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(fname)

    errors = []
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if errors:
        pytest.fail(" | ".join(errors))