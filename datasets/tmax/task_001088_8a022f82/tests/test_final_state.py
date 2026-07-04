# test_final_state.py

import os
import subprocess
import pytest

EXECUTABLE = "/home/user/config_filter"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} does not exist. Did you compile the C program?"
    assert os.access(EXECUTABLE, os.X_OK), f"File {EXECUTABLE} is not executable."

def test_corpus_filtering():
    if not os.path.isfile(EXECUTABLE):
        pytest.fail(f"Executable {EXECUTABLE} missing.")

    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    clean_failed = []
    for f in clean_files:
        res = subprocess.run([EXECUTABLE, f], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        res = subprocess.run([EXECUTABLE, f], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(f))

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: " + ", ".join(evil_failed))
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: " + ", ".join(clean_failed))

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))