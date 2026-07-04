# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/dedup_stream.sh"
CLEAN_DIR = "/home/user/corpora/clean"
EVIL_DIR = "/home/user/corpora/evil"
GOLDEN_EVIL_DIR = "/home/user/corpora/golden_evil"

def run_script(input_csv_path):
    with open(input_csv_path, 'r') as f:
        result = subprocess.run(
            ["bash", SCRIPT_PATH],
            stdin=f,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    return result

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"{SCRIPT_PATH} is not executable"

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]
    assert len(clean_files) > 0, "No clean corpus files found."

    modified_clean = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        with open(filepath, 'r') as f:
            expected_output = f.read()

        result = run_script(filepath)
        if result.returncode != 0 or result.stdout != expected_output:
            modified_clean.append(filename)

    assert not modified_clean, f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}"

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed_evil = []

    for filename in evil_files:
        evil_path = os.path.join(EVIL_DIR, filename)
        golden_path = os.path.join(GOLDEN_EVIL_DIR, filename)

        with open(golden_path, 'r') as f:
            expected_output = f.read()

        result = run_script(evil_path)
        if result.returncode != 0 or result.stdout != expected_output:
            bypassed_evil.append(filename)

    assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}"