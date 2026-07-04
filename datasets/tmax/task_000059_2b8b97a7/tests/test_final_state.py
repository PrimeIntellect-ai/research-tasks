# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/validate_logs.sh"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.csv"))

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_DIR}"
    assert len(evil_files) > 0, f"No evil files found in {EVIL_DIR}"

    clean_failed = []
    evil_bypassed = []

    for clean_file in clean_files:
        result = subprocess.run([SCRIPT_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(clean_file))

    for evil_file in evil_files:
        result = subprocess.run([SCRIPT_PATH, evil_file], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_file))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_bypassed)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))