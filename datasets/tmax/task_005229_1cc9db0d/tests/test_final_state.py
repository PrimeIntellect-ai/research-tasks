# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/verify_backup.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def test_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory {CLEAN_CORPUS_DIR} missing."
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))
    assert clean_files, f"No JSON files found in {CLEAN_CORPUS_DIR}."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected (expected exit 0). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory {EVIL_CORPUS_DIR} missing."
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))
    assert evil_files, f"No JSON files found in {EVIL_CORPUS_DIR}."

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed (expected non-zero exit). Offending files: {', '.join(bypassed_files)}")