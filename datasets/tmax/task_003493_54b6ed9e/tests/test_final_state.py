# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/validator/target/release/validator"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_validator_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Validator binary not found at {BINARY_PATH}. Did you compile it in release mode?"
    assert os.access(BINARY_PATH, os.X_OK), f"Validator binary at {BINARY_PATH} is not executable."

def test_clean_corpus_accepted():
    if not os.path.isfile(BINARY_PATH):
        pytest.skip("Validator binary not found.")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(('.yaml', '.yml'))]
    assert len(clean_files) > 0, f"No clean corpus files found in {CLEAN_CORPUS_DIR}."

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(filename)

    assert len(failed_files) == 0, (
        f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (modified/flagged). "
        f"Offending files: {', '.join(failed_files)}"
    )

def test_evil_corpus_rejected():
    if not os.path.isfile(BINARY_PATH):
        pytest.skip("Validator binary not found.")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(('.yaml', '.yml'))]
    assert len(evil_files) > 0, f"No evil corpus files found in {EVIL_CORPUS_DIR}."

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True)
        if result.returncode == 0:
            failed_files.append(filename)

    assert len(failed_files) == 0, (
        f"{len(failed_files)} of {len(evil_files)} evil files bypassed the check (were accepted). "
        f"Offending files: {', '.join(failed_files)}"
    )