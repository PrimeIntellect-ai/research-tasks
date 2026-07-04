# test_final_state.py

import os
import subprocess
import pytest

AGENT_BINARY = "/home/user/filter_etl"
CLEAN_CORPUS_DIR = "/verify/clean/"
EVIL_CORPUS_DIR = "/verify/evil/"

def test_binary_exists_and_executable():
    assert os.path.exists(AGENT_BINARY), f"The agent binary is missing at {AGENT_BINARY}"
    assert os.path.isfile(AGENT_BINARY), f"{AGENT_BINARY} is not a file"
    assert os.access(AGENT_BINARY, os.X_OK), f"The agent binary at {AGENT_BINARY} is not executable"

def test_clean_corpus():
    if not os.path.exists(CLEAN_CORPUS_DIR):
        pytest.fail(f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}")

    files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    if not files:
        pytest.fail(f"No files found in {CLEAN_CORPUS_DIR}")

    failed_files = []
    for f in files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, f)
        result = subprocess.run([AGENT_BINARY, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(files)} clean files rejected (expected exit code 0). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    if not os.path.exists(EVIL_CORPUS_DIR):
        pytest.fail(f"Evil corpus directory missing: {EVIL_CORPUS_DIR}")

    files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    if not files:
        pytest.fail(f"No files found in {EVIL_CORPUS_DIR}")

    failed_files = []
    for f in files:
        filepath = os.path.join(EVIL_CORPUS_DIR, f)
        result = subprocess.run([AGENT_BINARY, filepath], capture_output=True)
        if result.returncode == 0:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(files)} evil files bypassed (expected non-zero exit code). Offending files: {', '.join(failed_files)}")