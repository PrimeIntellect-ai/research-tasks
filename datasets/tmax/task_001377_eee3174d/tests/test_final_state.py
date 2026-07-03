# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/validate_config.sh"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing: {CLEAN_DIR}"
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.tar')]
    assert len(clean_files) > 0, "No clean tarballs found to test."

    failed_files = []
    for f in clean_files:
        path = os.path.join(CLEAN_DIR, f)
        result = subprocess.run(["bash", SCRIPT_PATH, path], capture_output=True)
        if result.returncode != 0:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected instead of accepted). Offending files: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory missing: {EVIL_DIR}"
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.tar')]
    assert len(evil_files) > 0, "No evil tarballs found to test."

    failed_files = []
    for f in evil_files:
        path = os.path.join(EVIL_DIR, f)
        result = subprocess.run(["bash", SCRIPT_PATH, path], capture_output=True)
        # The script must exit with a non-zero status for evil files
        if result.returncode == 0:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (accepted instead of rejected). Offending files: {', '.join(failed_files)}")