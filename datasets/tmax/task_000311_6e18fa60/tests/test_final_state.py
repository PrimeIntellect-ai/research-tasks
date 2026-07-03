# test_final_state.py

import os
import subprocess
import pytest

EXECUTABLE_PATH = "/home/user/audit_filter"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_executable_exists_and_is_executable():
    assert os.path.exists(EXECUTABLE_PATH), f"Executable not found at {EXECUTABLE_PATH}"
    assert os.path.isfile(EXECUTABLE_PATH), f"{EXECUTABLE_PATH} is not a file"
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"Executable at {EXECUTABLE_PATH} is not executable"

def test_clean_corpus_accepted():
    if not os.path.exists(CLEAN_CORPUS_DIR):
        pytest.fail(f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory"

    failures = []
    for filepath in clean_files:
        result = subprocess.run([EXECUTABLE_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            failures.append(os.path.basename(filepath))

    if failures:
        pytest.fail(f"{len(failures)} of {len(clean_files)} clean files rejected (should be accepted). Offending files: {', '.join(failures)}")

def test_evil_corpus_rejected():
    if not os.path.exists(EVIL_CORPUS_DIR):
        pytest.fail(f"Evil corpus directory missing: {EVIL_CORPUS_DIR}")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus directory"

    failures = []
    for filepath in evil_files:
        result = subprocess.run([EXECUTABLE_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            failures.append(os.path.basename(filepath))

    if failures:
        pytest.fail(f"{len(failures)} of {len(evil_files)} evil files bypassed (should be rejected). Offending files: {', '.join(failures)}")