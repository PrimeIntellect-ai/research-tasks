# test_final_state.py
import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/filter_backup.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script missing: {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script is not executable: {SCRIPT_PATH}"

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.sql"))
    assert len(clean_files) > 0, "No clean files found."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "CLEAN":
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected (should be accepted). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.sql"))
    assert len(evil_files) > 0, "No evil files found."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "EVIL":
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (should be rejected). Offending files: {', '.join(failed_files)}")