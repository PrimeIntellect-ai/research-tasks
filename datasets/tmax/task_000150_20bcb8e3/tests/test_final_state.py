# test_final_state.py

import os
import subprocess
import glob
import pytest

EXECUTABLE = "/home/user/sanitiser"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} does not exist. Did you compile the Go program?"
    assert os.access(EXECUTABLE, os.X_OK), f"File {EXECUTABLE} is not executable."

def test_clean_corpus_accepted():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*"))
    assert len(clean_files) > 0, f"No files found in {CLEAN_DIR}."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (non-zero exit code). Offending files: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*"))
    assert len(evil_files) > 0, f"No files found in {EVIL_DIR}."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True)
        if result.returncode == 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files incorrectly bypassed the sanitiser (zero exit code). Offending files: {', '.join(failed_files)}")