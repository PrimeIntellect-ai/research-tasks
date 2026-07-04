# test_final_state.py
import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/classifier.sh"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

def test_classifier_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"{SCRIPT_PATH} is not executable."

def test_clean_corpus():
    clean_files = sorted(glob.glob(os.path.join(CLEAN_DIR, "*")))
    assert len(clean_files) > 0, f"No files found in {CLEAN_DIR}"

    failed_files = []
    for fpath in clean_files:
        res = subprocess.run([SCRIPT_PATH, fpath], capture_output=True)
        if res.returncode != 0:
            failed_files.append(os.path.basename(fpath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected (should be accepted with exit code 0). "
                    f"Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    evil_files = sorted(glob.glob(os.path.join(EVIL_DIR, "*")))
    assert len(evil_files) > 0, f"No files found in {EVIL_DIR}"

    failed_files = []
    for fpath in evil_files:
        res = subprocess.run([SCRIPT_PATH, fpath], capture_output=True)
        if res.returncode == 0:
            failed_files.append(os.path.basename(fpath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (should be rejected with exit code 1). "
                    f"Offending files: {', '.join(failed_files)}")