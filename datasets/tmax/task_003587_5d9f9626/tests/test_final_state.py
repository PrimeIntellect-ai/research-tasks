# test_final_state.py

import os
import subprocess
import glob
import pytest

CLEAN_CORPUS_DIR = "/app/clean_corpus"
EVIL_CORPUS_DIR = "/app/evil_corpus"
EXECUTABLE_PATH = "/home/user/seq_filter/target/release/seq_filter"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE_PATH), f"Executable not found at {EXECUTABLE_PATH}. Did you build the Rust project in release mode?"
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"File at {EXECUTABLE_PATH} is not executable."

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.fasta"))
    assert len(clean_files) > 0, f"No clean corpus files found in {CLEAN_CORPUS_DIR}"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([EXECUTABLE_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected (expected exit code 0). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.fasta"))
    assert len(evil_files) > 0, f"No evil corpus files found in {EVIL_CORPUS_DIR}"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([EXECUTABLE_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (expected exit code 1). Offending files: {', '.join(failed_files)}")