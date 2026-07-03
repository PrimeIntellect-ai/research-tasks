# test_final_state.py
import os
import subprocess
import glob
import pytest

SCRIPT_PATH = "/home/user/verify_backup.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_clean_corpus():
    clean_tars = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.tar"))
    assert len(clean_tars) > 0, "No clean tarballs found."

    failed_files = []
    for tar in clean_tars:
        result = subprocess.run([SCRIPT_PATH, tar], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(tar))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_tars)} clean modified/rejected: {', '.join(failed_files)}")

def test_evil_corpus():
    evil_tars = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.tar"))
    assert len(evil_tars) > 0, "No evil tarballs found."

    bypassed_files = []
    for tar in evil_tars:
        result = subprocess.run([SCRIPT_PATH, tar], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(tar))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_tars)} evil bypassed: {', '.join(bypassed_files)}")