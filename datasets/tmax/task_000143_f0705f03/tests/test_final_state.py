# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/filter.sh"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory {EVIL_CORPUS_DIR} missing."
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory {CLEAN_CORPUS_DIR} missing."

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".gql")]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".gql")]

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    bypassed_evil = []
    for f in evil_files:
        result = subprocess.run([SCRIPT_PATH, f], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(f))

    modified_clean = []
    for f in clean_files:
        result = subprocess.run([SCRIPT_PATH, f], capture_output=True)
        if result.returncode != 0:
            modified_clean.append(os.path.basename(f))

    errors = []
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        errors.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(modified_clean)}")

    assert not errors, " | ".join(errors)