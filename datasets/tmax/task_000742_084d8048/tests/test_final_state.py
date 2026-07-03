# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/proto_filter.sh"
EVIL_DIR = "/test_data/evil"
CLEAN_DIR = "/test_data/clean"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory missing: {EVIL_DIR}"
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith(".proto")]
    assert len(evil_files) > 0, f"No .proto files found in {EVIL_DIR}"

    bypassed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed the filter (returned 0). Offending files: {', '.join(bypassed_files)}")

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing: {CLEAN_DIR}"
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith(".proto")]
    assert len(clean_files) > 0, f"No .proto files found in {CLEAN_DIR}"

    rejected_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            rejected_files.append(filename)

    if rejected_files:
        pytest.fail(f"{len(rejected_files)} of {len(clean_files)} clean files were incorrectly rejected (returned non-zero). Offending files: {', '.join(rejected_files)}")