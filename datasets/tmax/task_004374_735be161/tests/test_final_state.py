# test_final_state.py
import os
import subprocess
import pytest

CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"
SCRIPT_PATH = "/home/user/c2_ingress"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_adversarial_corpus():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory {CLEAN_DIR} is missing."
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory {EVIL_DIR} is missing."

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failures = []
    for clean_file in clean_files:
        result = subprocess.run([SCRIPT_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(clean_file))

    evil_failures = []
    for evil_file in evil_files:
        result = subprocess.run([SCRIPT_PATH, evil_file], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(evil_file))

    error_msg = ""
    if clean_failures:
        error_msg += f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}. "
    if evil_failures:
        error_msg += f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}."

    assert not clean_failures and not evil_failures, error_msg.strip()