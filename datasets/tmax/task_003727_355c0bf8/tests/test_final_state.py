# test_final_state.py

import os
import subprocess
import pytest

VALIDATOR_BIN = "/home/user/validator"
EVIL_DIR = "/home/user/payloads/evil"
CLEAN_DIR = "/home/user/payloads/clean"

def test_validator_binary_exists():
    assert os.path.isfile(VALIDATOR_BIN), f"Validator binary not found at {VALIDATOR_BIN}"
    assert os.access(VALIDATOR_BIN, os.X_OK), f"Validator binary at {VALIDATOR_BIN} is not executable"

def test_payload_directories_exist():
    assert os.path.isdir(EVIL_DIR), f"Evil payloads directory not found at {EVIL_DIR}. Did the agent decrypt and extract the archive correctly?"
    assert os.path.isdir(CLEAN_DIR), f"Clean payloads directory not found at {CLEAN_DIR}. Did the agent decrypt and extract the archive correctly?"

def test_adversarial_corpus():
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]

    assert len(evil_files) > 0, f"No files found in {EVIL_DIR}"
    assert len(clean_files) > 0, f"No files found in {CLEAN_DIR}"

    evil_bypassed = []
    clean_modified = []

    # Check evil corpus
    for filepath in evil_files:
        result = subprocess.run([VALIDATOR_BIN, filepath], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(filepath))

    # Check clean corpus
    for filepath in clean_files:
        result = subprocess.run([VALIDATOR_BIN, filepath], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(filepath))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean rejected: {', '.join(clean_modified)}")

    assert not evil_bypassed and not clean_modified, "Adversarial corpus validation failed:\n" + "\n".join(error_messages)