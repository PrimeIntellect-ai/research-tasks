# test_final_state.py

import os
import subprocess
import glob
import pytest

BINARY_PATH = "/home/user/sim_filter/target/release/sim_filter"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_binary_exists():
    """Verify that the compiled Rust binary exists at the specified path."""
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}. Did you compile in release mode?"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable."

def test_clean_corpus_accepted():
    """Verify that the binary accepts all clean corpus files (exit code 0)."""
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))
    assert len(clean_files) > 0, f"No clean corpus files found in {CLEAN_CORPUS_DIR}."

    failed_files = []
    for file_path in clean_files:
        result = subprocess.run([BINARY_PATH, file_path], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected incorrectly): {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    """Verify that the binary rejects all evil corpus files (exit code 1)."""
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))
    assert len(evil_files) > 0, f"No evil corpus files found in {EVIL_CORPUS_DIR}."

    failed_files = []
    for file_path in evil_files:
        result = subprocess.run([BINARY_PATH, file_path], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (accepted incorrectly): {', '.join(failed_files)}")