# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/app/validator/target/debug/validator"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_binary_exists():
    """Verify that the validator binary has been built."""
    assert os.path.isfile(BINARY_PATH), f"Validator binary not found at {BINARY_PATH}. Did the build fail?"
    assert os.access(BINARY_PATH, os.X_OK), f"Validator binary at {BINARY_PATH} is not executable."

def test_adversarial_corpus():
    """Verify that the validator correctly processes clean and evil corpora."""

    # Ensure corpora directories exist
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    assert len(clean_files) > 0, "Clean corpus is empty."
    assert len(evil_files) > 0, "Evil corpus is empty."

    clean_failures = []
    for clean_file in clean_files:
        result = subprocess.run([BINARY_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(clean_file))

    evil_failures = []
    for evil_file in evil_files:
        result = subprocess.run([BINARY_PATH, evil_file], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(evil_file))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))