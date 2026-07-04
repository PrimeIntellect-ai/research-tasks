# test_final_state.py

import os
import subprocess
import pytest

VALIDATOR_PATH = "/home/user/validator"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_validator_executable_exists():
    assert os.path.isfile(VALIDATOR_PATH), f"Validator executable not found at {VALIDATOR_PATH}"
    assert os.access(VALIDATOR_PATH, os.X_OK), f"Validator at {VALIDATOR_PATH} is not executable"

def test_adversarial_corpus():
    if not os.path.isfile(VALIDATOR_PATH) or not os.access(VALIDATOR_PATH, os.X_OK):
        pytest.fail(f"Cannot run tests: {VALIDATOR_PATH} is missing or not executable.")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".sql")]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".sql")]

    clean_failures = []
    evil_failures = []

    for clean_file in clean_files:
        try:
            result = subprocess.run([VALIDATOR_PATH, clean_file], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "ACCEPT":
                clean_failures.append((os.path.basename(clean_file), output, result.returncode))
        except Exception as e:
            clean_failures.append((os.path.basename(clean_file), str(e), -1))

    for evil_file in evil_files:
        try:
            result = subprocess.run([VALIDATOR_PATH, evil_file], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "REJECT":
                evil_failures.append((os.path.basename(evil_file), output, result.returncode))
        except Exception as e:
            evil_failures.append((os.path.basename(evil_file), str(e), -1))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected:")
        for f, out, rc in clean_failures:
            error_messages.append(f"  - {f} (output: {out!r}, exit: {rc})")

    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted:")
        for f, out, rc in evil_failures:
            error_messages.append(f"  - {f} (output: {out!r}, exit: {rc})")

    if error_messages:
        pytest.fail("\n".join(error_messages))