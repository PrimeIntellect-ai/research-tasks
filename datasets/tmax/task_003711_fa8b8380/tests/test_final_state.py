# test_final_state.py
import os
import glob
import subprocess
import pytest

EXECUTABLE = "/home/user/validator"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_executable_exists_and_is_runnable():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}. Did you compile your C++ code?"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable."

def test_adversarial_corpus_validation():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json.gz"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json.gz"))

    assert len(clean_files) > 0, f"No clean corpus files found in {CLEAN_CORPUS_DIR}"
    assert len(evil_files) > 0, f"No evil corpus files found in {EVIL_CORPUS_DIR}"

    clean_rejected = []
    for clean_file in clean_files:
        result = subprocess.run([EXECUTABLE, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(clean_file))

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run([EXECUTABLE, evil_file], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_file))

    errors = []
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean rejected: {', '.join(clean_rejected)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))