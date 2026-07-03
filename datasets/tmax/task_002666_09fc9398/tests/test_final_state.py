# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/verify_archive.py"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

def run_script(zip_path):
    result = subprocess.run(
        ["python3", SCRIPT_PATH, zip_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.returncode

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.zip')]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for f in clean_files:
        zip_path = os.path.join(CLEAN_CORPUS_DIR, f)
        exit_code = run_script(zip_path)
        if exit_code != 0:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}")

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.zip')]
    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed_files = []
    for f in evil_files:
        zip_path = os.path.join(EVIL_CORPUS_DIR, f)
        exit_code = run_script(zip_path)
        if exit_code == 0:
            bypassed_files.append(f)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")