# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/config_gate.py"
CLEAN_DIR = "/app/tests/clean"
EVIL_DIR = "/app/tests/evil"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

def test_clean_corpus():
    assert os.path.exists(CLEAN_DIR), f"Clean corpus directory {CLEAN_DIR} is missing."
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith('.cfg')]
    assert len(clean_files) > 0, "No clean configuration files found."

    failed_files = []
    for cfg_file in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, cfg_file], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(cfg_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (exit code != 0). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    assert os.path.exists(EVIL_DIR), f"Evil corpus directory {EVIL_DIR} is missing."
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith('.cfg')]
    assert len(evil_files) > 0, "No evil configuration files found."

    failed_files = []
    for cfg_file in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, cfg_file], capture_output=True)
        if result.returncode == 0:
            failed_files.append(os.path.basename(cfg_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed validation (exit code == 0). Offending files: {', '.join(failed_files)}")