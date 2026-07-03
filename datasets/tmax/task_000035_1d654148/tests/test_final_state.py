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

def test_adversarial_corpus():
    if not os.path.isfile(SCRIPT_PATH):
        pytest.fail(f"Cannot run test: {SCRIPT_PATH} does not exist.")

    # Check clean corpus
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert clean_files, f"No JSON files found in {CLEAN_CORPUS_DIR}"

    clean_failures = []
    for fpath in clean_files:
        result = subprocess.run(["bash", SCRIPT_PATH, fpath], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(fpath))

    # Check evil corpus
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert evil_files, f"No JSON files found in {EVIL_CORPUS_DIR}"

    evil_failures = []
    for fpath in evil_files:
        result = subprocess.run(["bash", SCRIPT_PATH, fpath], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(fpath))

    errors = []
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean payloads were incorrectly rejected: {', '.join(clean_failures)}")

    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil payloads bypassed the filter: {', '.join(evil_failures)}")

    if errors:
        pytest.fail(" | ".join(errors))