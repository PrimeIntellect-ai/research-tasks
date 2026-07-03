# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/classifier.sh"
CLEAN_CORPUS_DIR = "/app/test_clean"
EVIL_CORPUS_DIR = "/app/test_evil"

def test_classifier_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Classifier script missing at {SCRIPT_PATH}"

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(["bash", SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected (should be accepted/exit 0). Offending files: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(["bash", SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (should be rejected/exit 1). Offending files: {', '.join(failed_files)}")