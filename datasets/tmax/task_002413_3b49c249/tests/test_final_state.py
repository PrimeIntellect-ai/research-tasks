# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = '/home/user/log_classifier.py'
CLEAN_DIR = '/app/corpora/clean'
EVIL_DIR = '/app/corpora/evil'

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_clean_corpus():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory {CLEAN_DIR} missing."
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]
    assert len(clean_files) > 0, "No clean files found in corpus."

    failed_files = []
    for f in clean_files:
        filepath = os.path.join(CLEAN_DIR, f)
        res = subprocess.run(['python3', SCRIPT_PATH, filepath], capture_output=True)
        if res.returncode != 0:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory {EVIL_DIR} missing."
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    assert len(evil_files) > 0, "No evil files found in corpus."

    failed_files = []
    for f in evil_files:
        filepath = os.path.join(EVIL_DIR, f)
        res = subprocess.run(['python3', SCRIPT_PATH, filepath], capture_output=True)
        if res.returncode != 1:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_files)}")