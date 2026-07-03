# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/chunk_filter.py"
CLEAN_CORPUS_DIR = "/validation/clean"
EVIL_CORPUS_DIR = "/validation/evil"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Missing script: {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Not a file: {SCRIPT_PATH}"

def test_clean_corpus():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Missing clean corpus directory: {CLEAN_CORPUS_DIR}"
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, f"No files found in clean corpus: {CLEAN_CORPUS_DIR}"

    failed_files = []
    for fpath in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, fpath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(fpath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected with exit code != 0). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Missing evil corpus directory: {EVIL_CORPUS_DIR}"
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, f"No files found in evil corpus: {EVIL_CORPUS_DIR}"

    bypassed_files = []
    for fpath in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, fpath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(fpath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed (accepted with exit code != 1). Offending files: {', '.join(bypassed_files)}")