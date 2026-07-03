# test_final_state.py

import os
import subprocess
import glob
import pytest

BINARY_PATH = "/home/user/backup_validator/target/release/backup_validator"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def test_clean_corpus():
    clean_files = sorted(glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json")))
    assert len(clean_files) > 0, f"No clean corpus files found in {CLEAN_CORPUS_DIR}"

    failed_files = []
    for f in clean_files:
        result = subprocess.run([BINARY_PATH, f], capture_output=True, text=True)
        if result.returncode != 0 or "ACCEPT" not in result.stdout:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected instead of accepted): {', '.join(failed_files)}")

def test_evil_corpus():
    evil_files = sorted(glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json")))
    assert len(evil_files) > 0, f"No evil corpus files found in {EVIL_CORPUS_DIR}"

    bypassed_files = []
    for f in evil_files:
        result = subprocess.run([BINARY_PATH, f], capture_output=True, text=True)
        if result.returncode != 1 or "REJECT" not in result.stdout:
            bypassed_files.append(os.path.basename(f))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed (accepted instead of rejected): {', '.join(bypassed_files)}")