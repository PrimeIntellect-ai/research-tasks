# test_final_state.py

import os
import subprocess
import pytest

def test_agent_binary_exists_and_executable():
    cpp_path = "/home/user/detector.cpp"
    binary_path = "/home/user/detector"

    assert os.path.exists(cpp_path), f"The source code is missing at {cpp_path}"
    assert os.path.exists(binary_path), f"The compiled binary is missing at {binary_path}"
    assert os.path.isfile(binary_path), f"The path {binary_path} is not a file"
    assert os.access(binary_path, os.X_OK), f"The binary at {binary_path} is not executable"

def test_evil_corpus_rejected():
    binary_path = "/home/user/detector"
    evil_corpus_path = "/app/corpus/evil/"

    evil_files = [f for f in os.listdir(evil_corpus_path) if f.endswith('.csv')]
    assert len(evil_files) > 0, "No CSV files found in the evil corpus directory."

    bypassed_files = []

    for filename in evil_files:
        filepath = os.path.join(evil_corpus_path, filename)
        result = subprocess.run([binary_path, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed (expected exit code 1, got something else). Offending files: {', '.join(bypassed_files)}")

def test_clean_corpus_accepted():
    binary_path = "/home/user/detector"
    clean_corpus_path = "/app/corpus/clean/"

    clean_files = [f for f in os.listdir(clean_corpus_path) if f.endswith('.csv')]
    assert len(clean_files) > 0, "No CSV files found in the clean corpus directory."

    modified_files = []

    for filename in clean_files:
        filepath = os.path.join(clean_corpus_path, filename)
        result = subprocess.run([binary_path, filepath], capture_output=True)
        if result.returncode != 0:
            modified_files.append(filename)

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified (expected exit code 0, got something else). Offending files: {', '.join(modified_files)}")