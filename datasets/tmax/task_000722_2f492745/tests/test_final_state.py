# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/filter_artifacts.sh"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"The script {SCRIPT_PATH} is not executable."

def test_clean_corpus():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory {CLEAN_DIR} is missing."
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.tar.gz')]
    assert len(clean_files) > 0, f"No .tar.gz files found in {CLEAN_DIR}."

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        result = subprocess.run(["bash", SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory {EVIL_DIR} is missing."
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.tar.gz')]
    assert len(evil_files) > 0, f"No .tar.gz files found in {EVIL_DIR}."

    bypassed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        result = subprocess.run(["bash", SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed_files)}")