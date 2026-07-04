# test_final_state.py

import os
import subprocess
import pytest

ENTRY_POINT = "/home/user/audit_filter.sh"
CLEAN_CORPUS = "/app/eval_corpus/clean"
EVIL_CORPUS = "/app/eval_corpus/evil"

def test_script_exists_and_executable():
    assert os.path.isfile(ENTRY_POINT), f"The script {ENTRY_POINT} does not exist."
    assert os.access(ENTRY_POINT, os.X_OK), f"The script {ENTRY_POINT} is not executable."

def test_clean_corpus_preserved():
    """Ensure the script exits with 0 for all legitimate tokens."""
    if not os.path.isdir(CLEAN_CORPUS):
        pytest.fail(f"Clean corpus directory missing: {CLEAN_CORPUS}")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    if not clean_files:
        pytest.fail(f"No files found in clean corpus directory: {CLEAN_CORPUS}")

    failed_files = []
    total = len(clean_files)

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS, filename)
        result = subprocess.run([ENTRY_POINT, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {total} clean modified/rejected (expected exit 0). Offending files: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    """Ensure the script exits with 1 for all forged tokens."""
    if not os.path.isdir(EVIL_CORPUS):
        pytest.fail(f"Evil corpus directory missing: {EVIL_CORPUS}")

    evil_files = [f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    if not evil_files:
        pytest.fail(f"No files found in evil corpus directory: {EVIL_CORPUS}")

    failed_files = []
    total = len(evil_files)

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS, filename)
        result = subprocess.run([ENTRY_POINT, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {total} evil bypassed (expected exit 1). Offending files: {', '.join(failed_files)}")