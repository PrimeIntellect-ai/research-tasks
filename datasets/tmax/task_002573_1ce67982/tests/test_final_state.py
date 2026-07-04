# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/project/bin/log_sanitizer"
CLEAN_CORPUS_DIR = "/app/hidden_eval/clean"
EVIL_CORPUS_DIR = "/app/hidden_eval/evil"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Executable not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"File at {BINARY_PATH} is not executable"

def test_clean_corpus():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.skip(f"Clean corpus directory {CLEAN_CORPUS_DIR} not found")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.skip(f"Evil corpus directory {EVIL_CORPUS_DIR} not found")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_files)}")