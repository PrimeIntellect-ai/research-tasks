# test_final_state.py

import os
import subprocess
import pytest

VALIDATOR_PATH = "/home/user/validator"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_validator_exists_and_executable():
    assert os.path.isfile(VALIDATOR_PATH), f"Validator binary not found at {VALIDATOR_PATH}"
    assert os.access(VALIDATOR_PATH, os.X_OK), f"Validator binary at {VALIDATOR_PATH} is not executable"

def test_clean_corpus():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.fail(f"Clean corpus directory missing at {CLEAN_CORPUS_DIR}")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.sql')]
    if not clean_files:
        pytest.fail("No SQL files found in clean corpus.")

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run([VALIDATOR_PATH, filepath], capture_output=True, text=True)
        if result.returncode != 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean queries rejected (expected to pass): {', '.join(failed_files)}")

def test_evil_corpus():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.fail(f"Evil corpus directory missing at {EVIL_CORPUS_DIR}")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.sql')]
    if not evil_files:
        pytest.fail("No SQL files found in evil corpus.")

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run([VALIDATOR_PATH, filepath], capture_output=True, text=True)
        if result.returncode == 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil queries bypassed (expected to fail): {', '.join(failed_files)}")