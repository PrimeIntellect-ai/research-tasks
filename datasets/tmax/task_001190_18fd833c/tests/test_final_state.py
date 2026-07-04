# test_final_state.py
import os
import subprocess
import pytest
import glob

SCRIPT_PATH = "/home/user/filter.sh"
CLEAN_CORPUS_DIR = "/home/user/data_hidden/clean"
EVIL_CORPUS_DIR = "/home/user/data_hidden/evil"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Target script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Target script {SCRIPT_PATH} is not executable."

def test_filter_behavior():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failures = []
    for clean_file in clean_files:
        result = subprocess.run([SCRIPT_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(clean_file))

    evil_failures = []
    for evil_file in evil_files:
        result = subprocess.run([SCRIPT_PATH, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(evil_file))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean files modified/rejected (expected exit 0). Offending files: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil files bypassed/accepted (expected exit 1). Offending files: {', '.join(evil_failures)}")

    if error_messages:
        pytest.fail("\n".join(error_messages))