# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/filter.sh"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_script_exists_and_executable():
    """Verify that the student's script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    # Even if not executable, we run it with `bash`, but it's good practice to check if it's a file

def test_clean_corpus_preserved():
    """Verify that all clean logs are accepted (exit code 0)."""
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus directory missing: {CLEAN_CORPUS}"

    clean_files = [
        os.path.join(CLEAN_CORPUS, f) 
        for f in os.listdir(CLEAN_CORPUS) 
        if os.path.isfile(os.path.join(CLEAN_CORPUS, f))
    ]
    assert len(clean_files) > 0, f"No files found in clean corpus directory: {CLEAN_CORPUS}"

    modified = []
    for filepath in clean_files:
        result = subprocess.run(["bash", SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            modified.append(os.path.basename(filepath))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified: {', '.join(modified)}")

def test_evil_corpus_rejected():
    """Verify that all evil logs are rejected (exit code 1)."""
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus directory missing: {EVIL_CORPUS}"

    evil_files = [
        os.path.join(EVIL_CORPUS, f) 
        for f in os.listdir(EVIL_CORPUS) 
        if os.path.isfile(os.path.join(EVIL_CORPUS, f))
    ]
    assert len(evil_files) > 0, f"No files found in evil corpus directory: {EVIL_CORPUS}"

    bypassed = []
    for filepath in evil_files:
        result = subprocess.run(["bash", SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed.append(os.path.basename(filepath))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")