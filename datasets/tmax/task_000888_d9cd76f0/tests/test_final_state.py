# test_final_state.py
import os
import subprocess
import pytest

EXECUTABLE_PATH = "/home/user/profile_analyzer"
CLEAN_CORPUS_DIR = "/app/corpora_hidden/clean"
EVIL_CORPUS_DIR = "/app/corpora_hidden/evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE_PATH), f"Executable not found at {EXECUTABLE_PATH}"
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"File at {EXECUTABLE_PATH} is not executable"

def test_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory"

    failures = []
    for filepath in clean_files:
        result = subprocess.run([EXECUTABLE_PATH, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "CLEAN":
            failures.append(os.path.basename(filepath))

    if failures:
        pytest.fail(f"{len(failures)} of {len(clean_files)} clean files misclassified (should be CLEAN). Offending files: {', '.join(failures)}")

def test_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus directory"

    failures = []
    for filepath in evil_files:
        result = subprocess.run([EXECUTABLE_PATH, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "EVIL":
            failures.append(os.path.basename(filepath))

    if failures:
        pytest.fail(f"{len(failures)} of {len(evil_files)} evil files bypassed (should be EVIL). Offending files: {', '.join(failures)}")