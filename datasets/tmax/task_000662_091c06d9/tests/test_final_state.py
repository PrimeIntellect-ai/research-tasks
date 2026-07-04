# test_final_state.py

import os
import glob
import subprocess
import pytest

BINARY_PATH = "/home/user/filter_logs/target/release/filter_logs"
CLEAN_DIR = "/app/clean"
EVIL_DIR = "/app/evil"

def test_binary_exists():
    assert os.path.exists(BINARY_PATH), f"Executable not found at {BINARY_PATH}"
    assert os.path.isfile(BINARY_PATH), f"{BINARY_PATH} is not a file"
    assert os.access(BINARY_PATH, os.X_OK), f"{BINARY_PATH} is not executable"

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.csv"))

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_DIR}"
    assert len(evil_files) > 0, f"No evil files found in {EVIL_DIR}"

    clean_failed = []
    for f in clean_files:
        result = subprocess.run([BINARY_PATH, f], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        result = subprocess.run([BINARY_PATH, f], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(f))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean files modified/rejected (expected exit 0). Offending files: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil files bypassed (expected exit 1). Offending files: {', '.join(evil_failed)}")

    if errors:
        pytest.fail("Adversarial corpus validation failed:\n" + "\n".join(errors))