# test_final_state.py

import os
import subprocess
import pytest

EXECUTABLE = "/home/user/backup_sanitizer"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} does not exist."
    assert os.access(EXECUTABLE, os.X_OK), f"Executable {EXECUTABLE} is not executable."

def test_adversarial_corpus():
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for f in clean_files:
        result = subprocess.run([EXECUTABLE, f], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        result = subprocess.run([EXECUTABLE, f], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(f))

    errors = []
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))