# test_final_state.py
import os
import subprocess
import pytest

VALIDATOR_PATH = "/home/user/validator"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_validator_exists_and_executable():
    assert os.path.isfile(VALIDATOR_PATH), f"Validator executable not found at {VALIDATOR_PATH}"
    assert os.access(VALIDATOR_PATH, os.X_OK), f"Validator at {VALIDATOR_PATH} is not executable"

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, f"No JSON files found in {CLEAN_CORPUS_DIR}"

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(filepath, 'r') as f:
            result = subprocess.run([VALIDATOR_PATH], stdin=f, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode != 0:
                failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected (should exit 0): {', '.join(failed_files)}")

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, f"No JSON files found in {EVIL_CORPUS_DIR}"

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        with open(filepath, 'r') as f:
            result = subprocess.run([VALIDATOR_PATH], stdin=f, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (should exit 1): {', '.join(failed_files)}")