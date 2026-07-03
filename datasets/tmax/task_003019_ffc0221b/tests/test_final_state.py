# test_final_state.py

import os
import subprocess
import pytest

FILTER_BIN = "/home/user/filter_signal"
EVIL_CORPUS = "/app/corpus/evil"
CLEAN_CORPUS = "/app/corpus/clean"

def test_filter_binary_exists():
    assert os.path.exists(FILTER_BIN), f"Expected compiled binary at {FILTER_BIN} does not exist."
    assert os.path.isfile(FILTER_BIN), f"{FILTER_BIN} is not a file."
    assert os.access(FILTER_BIN, os.X_OK), f"{FILTER_BIN} is not executable."

def test_evil_corpus_rejected():
    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    assert len(evil_files) > 0, "No files found in evil corpus."

    bypassed = []
    for fpath in evil_files:
        result = subprocess.run([FILTER_BIN, fpath], capture_output=True, text=True)
        if result.returncode != 1:
            bypassed.append(os.path.basename(fpath))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil files bypassed the filter: {', '.join(bypassed)}")

def test_clean_corpus_accepted():
    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    assert len(clean_files) > 0, "No files found in clean corpus."

    modified = []
    for fpath in clean_files:
        result = subprocess.run([FILTER_BIN, fpath], capture_output=True, text=True)
        if result.returncode != 0:
            modified.append(os.path.basename(fpath))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean files were rejected by the filter: {', '.join(modified)}")