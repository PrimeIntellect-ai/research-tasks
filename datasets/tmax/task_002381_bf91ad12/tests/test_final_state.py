# test_final_state.py

import os
import subprocess
import pytest

VALIDATOR_BIN = "/home/user/validator"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_validator_exists_and_executable():
    assert os.path.isfile(VALIDATOR_BIN), f"The binary {VALIDATOR_BIN} does not exist."
    assert os.access(VALIDATOR_BIN, os.X_OK), f"The binary {VALIDATOR_BIN} is not executable."

def test_adversarial_corpus():
    # Ensure binary exists first
    if not (os.path.isfile(VALIDATOR_BIN) and os.access(VALIDATOR_BIN, os.X_OK)):
        pytest.fail(f"Validator binary {VALIDATOR_BIN} is missing or not executable.")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_clean = []
    for clean_file in clean_files:
        result = subprocess.run([VALIDATOR_BIN, clean_file], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(clean_file))

    failed_evil = []
    for evil_file in evil_files:
        result = subprocess.run([VALIDATOR_BIN, evil_file], capture_output=True)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(evil_file))

    errors = []
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(failed_clean)}")

    if errors:
        pytest.fail(" | ".join(errors))