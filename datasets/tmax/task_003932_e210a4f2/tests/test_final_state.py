# test_final_state.py

import os
import subprocess
import pytest

FILTER_BIN = "/home/user/filter"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_filter_executable_exists():
    assert os.path.isfile(FILTER_BIN), f"Filter binary not found at {FILTER_BIN}. Did you compile your code?"
    assert os.access(FILTER_BIN, os.X_OK), f"Filter binary at {FILTER_BIN} is not executable."

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus directory missing: {CLEAN_CORPUS}"
    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    assert len(clean_files) > 0, "No files found in clean corpus."

    rejected = []
    for fpath in clean_files:
        with open(fpath, "rb") as f:
            result = subprocess.run([FILTER_BIN], stdin=f, capture_output=True)
        if result.returncode != 0:
            rejected.append(os.path.basename(fpath))

    assert not rejected, f"{len(rejected)} of {len(clean_files)} clean files rejected (expected exit code 0). Offending files: {', '.join(rejected)}"

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus directory missing: {EVIL_CORPUS}"
    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    assert len(evil_files) > 0, "No files found in evil corpus."

    accepted = []
    for fpath in evil_files:
        with open(fpath, "rb") as f:
            result = subprocess.run([FILTER_BIN], stdin=f, capture_output=True)
        if result.returncode != 1:
            accepted.append(os.path.basename(fpath))

    assert not accepted, f"{len(accepted)} of {len(evil_files)} evil files bypassed (expected exit code 1). Offending files: {', '.join(accepted)}"