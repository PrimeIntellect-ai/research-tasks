# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/archiver_cleanup/target/release/log_filter"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_binary_exists():
    """Check that the compiled Rust binary exists."""
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}. Did you run 'cargo build --release'?"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable."

def test_evil_corpus_rejected():
    """Check that all files in the evil corpus are rejected (exit code 1)."""
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing at {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus."

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed (expected exit code 1, got something else):\n" + "\n".join(bypassed_files))

def test_clean_corpus_accepted():
    """Check that all files in the clean corpus are accepted (exit code 0)."""
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing at {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus."

    rejected_files = []
    for filepath in clean_files:
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            rejected_files.append(os.path.basename(filepath))

    if rejected_files:
        pytest.fail(f"{len(rejected_files)} of {len(clean_files)} clean files rejected (expected exit code 0, got something else):\n" + "\n".join(rejected_files))