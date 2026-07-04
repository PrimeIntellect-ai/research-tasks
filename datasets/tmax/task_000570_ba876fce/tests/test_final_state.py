# test_final_state.py

import os
import glob
import subprocess
import pytest

EXECUTABLE = '/home/user/query_sanitizer'
CLEAN_CORPUS_DIR = '/app/corpus/clean'
EVIL_CORPUS_DIR = '/app/corpus/evil'

def test_executable_exists_and_is_executable():
    assert os.path.exists(EXECUTABLE), f"Executable {EXECUTABLE} does not exist."
    assert os.path.isfile(EXECUTABLE), f"{EXECUTABLE} is not a file."
    assert os.access(EXECUTABLE, os.X_OK), f"{EXECUTABLE} is not executable."

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, '*'))
    assert len(clean_files) > 0, f"No files found in clean corpus directory {CLEAN_CORPUS_DIR}."

    failed_files = []
    for filepath in clean_files:
        if not os.path.isfile(filepath):
            continue
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    total = len(clean_files)
    failed_count = len(failed_files)

    assert failed_count == 0, f"{failed_count} of {total} clean queries were rejected (expected 0). Offending files: {', '.join(failed_files)}"

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, '*'))
    assert len(evil_files) > 0, f"No files found in evil corpus directory {EVIL_CORPUS_DIR}."

    bypassed_files = []
    for filepath in evil_files:
        if not os.path.isfile(filepath):
            continue
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(filepath))

    total = len(evil_files)
    bypassed_count = len(bypassed_files)

    assert bypassed_count == 0, f"{bypassed_count} of {total} evil queries bypassed the sanitizer (expected 0). Offending files: {', '.join(bypassed_files)}"