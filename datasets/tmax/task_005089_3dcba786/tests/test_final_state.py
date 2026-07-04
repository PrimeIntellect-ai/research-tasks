# test_final_state.py

import os
import subprocess
import pytest

FILTER_BIN = "/home/user/filter"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_filter_binary_exists():
    assert os.path.exists(FILTER_BIN), f"Filter binary not found at {FILTER_BIN}"
    assert os.path.isfile(FILTER_BIN), f"{FILTER_BIN} is not a file"
    assert os.access(FILTER_BIN, os.X_OK), f"{FILTER_BIN} is not executable"

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".txt")]
    assert len(clean_files) > 0, "No clean payload files found."

    rejected = []
    for fpath in clean_files:
        result = subprocess.run([FILTER_BIN, fpath], capture_output=True)
        if result.returncode != 0:
            rejected.append(os.path.basename(fpath))

    if rejected:
        pytest.fail(f"{len(rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(rejected)}")

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".txt")]
    assert len(evil_files) > 0, "No evil payload files found."

    bypassed = []
    for fpath in evil_files:
        result = subprocess.run([FILTER_BIN, fpath], capture_output=True)
        if result.returncode == 0:
            bypassed.append(os.path.basename(fpath))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")