# test_final_state.py
import os
import subprocess
import pytest

FILTER_EXEC = "/home/user/filter"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_executable_exists():
    assert os.path.isfile(FILTER_EXEC), f"Executable {FILTER_EXEC} not found. Did you compile your C program?"
    assert os.access(FILTER_EXEC, os.X_OK), f"File {FILTER_EXEC} is not executable."

def test_corpus_evaluation():
    if not os.path.isfile(FILTER_EXEC) or not os.access(FILTER_EXEC, os.X_OK):
        pytest.fail("Filter executable is missing or not executable.")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    assert len(clean_files) > 0, "No clean files found in corpus."
    assert len(evil_files) > 0, "No evil files found in corpus."

    failed_clean = []
    for cf in clean_files:
        res = subprocess.run([FILTER_EXEC, cf], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        res = subprocess.run([FILTER_EXEC, ef], capture_output=True)
        if res.returncode != 1:
            failed_evil.append(os.path.basename(ef))

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean files rejected (expected to be accepted/exit 0): {failed_clean}")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil files bypassed (expected to be rejected/exit 1): {failed_evil}")

    if errors:
        pytest.fail(" | ".join(errors))