# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/audit_filter/target/release/audit_filter"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Expected binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def test_adversarial_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.txt')]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.txt')]

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failed = []
    for fpath in clean_files:
        result = subprocess.run([BINARY_PATH, fpath], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(fpath))

    evil_failed = []
    for fpath in evil_files:
        result = subprocess.run([BINARY_PATH, fpath], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(fpath))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))