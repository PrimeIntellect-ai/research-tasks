# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/analyze_graph.sh"
CLEAN_CORPUS_DIR = "/app/tests/corpus/clean"
EVIL_CORPUS_DIR = "/app/tests/corpus/evil"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Expected a file at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_adversarial_corpus():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))

    assert clean_files, f"No clean CSV files found in {CLEAN_CORPUS_DIR}"
    assert evil_files, f"No evil CSV files found in {EVIL_CORPUS_DIR}"

    clean_failures = []
    for f in clean_files:
        result = subprocess.run(["bash", SCRIPT_PATH, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run(["bash", SCRIPT_PATH, f], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(f))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))