# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/detect.py"
CLEAN_CORPUS_DIR = "/tmp/clean_corpus"
EVIL_CORPUS_DIR = "/tmp/evil_corpus"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Expected script at {SCRIPT_PATH} does not exist."

def test_adversarial_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus dir {CLEAN_CORPUS_DIR} missing."
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus dir {EVIL_CORPUS_DIR} missing."

    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.log"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.log"))

    assert len(clean_files) > 0, "No clean log files found."
    assert len(evil_files) > 0, "No evil log files found."

    clean_failures = []
    for f in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append((os.path.basename(f), result.returncode, result.stderr.decode('utf-8')))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, f], capture_output=True)
        if result.returncode != 1:
            evil_failures.append((os.path.basename(f), result.returncode, result.stderr.decode('utf-8')))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed:")
        for name, code, err in evil_failures:
            error_msgs.append(f"  - {name} (exit code {code})")

    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected:")
        for name, code, err in clean_failures:
            error_msgs.append(f"  - {name} (exit code {code})")

    if error_msgs:
        pytest.fail("\n".join(error_msgs))