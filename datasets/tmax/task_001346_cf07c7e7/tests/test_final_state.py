# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/artifact_filter"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary {BINARY_PATH} is missing."
    assert os.access(BINARY_PATH, os.X_OK), f"Binary {BINARY_PATH} is not executable."

def test_clean_corpus():
    # Get initial .bin files
    initial_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.bin')]
    assert len(initial_files) > 0, f"No .bin files found in {CLEAN_CORPUS_DIR} before execution."

    # Run the binary
    result = subprocess.run([BINARY_PATH, CLEAN_CORPUS_DIR], capture_output=True, text=True)
    assert result.returncode == 0, f"Binary execution failed on clean corpus: {result.stderr}"

    stdout_lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]

    # Check output and file renaming
    failed_files = []
    for f in initial_files:
        expected_output = f"{f}: CLEAN"
        if expected_output not in stdout_lines:
            failed_files.append(f)

        expected_renamed_path = os.path.join(CLEAN_CORPUS_DIR, f"{f}.clean")
        if not os.path.isfile(expected_renamed_path):
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(set(failed_files))} of {len(initial_files)} clean files modified/rejected (expected CLEAN). Offending files: {', '.join(set(failed_files))}")

def test_evil_corpus():
    # Get initial .bin files
    initial_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.bin')]
    assert len(initial_files) > 0, f"No .bin files found in {EVIL_CORPUS_DIR} before execution."

    # Run the binary
    result = subprocess.run([BINARY_PATH, EVIL_CORPUS_DIR], capture_output=True, text=True)
    assert result.returncode == 0, f"Binary execution failed on evil corpus: {result.stderr}"

    stdout_lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]

    # Check output and file renaming
    failed_files = []
    for f in initial_files:
        expected_output = f"{f}: EVIL"
        if expected_output not in stdout_lines:
            failed_files.append(f)

        expected_renamed_path = os.path.join(EVIL_CORPUS_DIR, f"{f}.evil")
        if not os.path.isfile(expected_renamed_path):
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(set(failed_files))} of {len(initial_files)} evil files bypassed (expected EVIL). Offending files: {', '.join(set(failed_files))}")