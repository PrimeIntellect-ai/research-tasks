# test_final_state.py

import os
import subprocess
import pytest

EXECUTABLE = "/home/user/query_filter"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus directory missing at {CLEAN_CORPUS}"
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.cql')]
    assert len(clean_files) > 0, "No clean corpus files found"

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS, filename)
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}"

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus directory missing at {EVIL_CORPUS}"
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith('.cql')]
    assert len(evil_files) > 0, "No evil corpus files found"

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS, filename)
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True)
        if result.returncode == 0:
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_files)}"