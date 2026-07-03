# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/filter_backups.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Expected script {SCRIPT_PATH} to exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Expected script {SCRIPT_PATH} to be executable."

def test_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory {CLEAN_CORPUS_DIR} missing."

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR)]
    assert clean_files, "Clean corpus is empty, cannot perform test."

    failed_files = []
    for file_path in clean_files:
        result = subprocess.run([SCRIPT_PATH, file_path], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected (expected exit code 0). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory {EVIL_CORPUS_DIR} missing."

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR)]
    assert evil_files, "Evil corpus is empty, cannot perform test."

    failed_files = []
    for file_path in evil_files:
        result = subprocess.run([SCRIPT_PATH, file_path], capture_output=True)
        if result.returncode == 0:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected exit code 1). Offending files: {', '.join(failed_files)}")