# test_final_state.py

import os
import subprocess
import pytest

CLEAN_CORPUS_DIR = "/app/clean_corpus"
EVIL_CORPUS_DIR = "/app/evil_corpus"
SCRIPT_PATH = "/home/user/etl_filter.py"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Directory {CLEAN_CORPUS_DIR} missing."
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, f"No JSON files found in {CLEAN_CORPUS_DIR}."

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run(["python3", SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Directory {EVIL_CORPUS_DIR} missing."
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, f"No JSON files found in {EVIL_CORPUS_DIR}."

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run(["python3", SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode == 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed/accepted. Offending files: {', '.join(failed_files)}")