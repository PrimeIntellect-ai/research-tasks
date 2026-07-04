# test_final_state.py
import os
import subprocess
import pytest

CLASSIFIER_SCRIPT = "/home/user/classifier.py"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def test_classifier_exists():
    assert os.path.isfile(CLASSIFIER_SCRIPT), f"Classifier script not found at {CLASSIFIER_SCRIPT}"

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing: {CLEAN_DIR}"
    clean_files = sorted([f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))])
    assert len(clean_files) > 0, "No clean files found in corpus."

    failed_files = []
    for fname in clean_files:
        fpath = os.path.join(CLEAN_DIR, fname)
        result = subprocess.run(["python3", CLASSIFIER_SCRIPT, fpath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(fname)

    if failed_files:
        pytest.fail(
            f"{len(failed_files)} of {len(clean_files)} clean modified/rejected (expected exit 0). "
            f"Offending files: {', '.join(failed_files)}"
        )

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory missing: {EVIL_DIR}"
    evil_files = sorted([f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))])
    assert len(evil_files) > 0, "No evil files found in corpus."

    failed_files = []
    for fname in evil_files:
        fpath = os.path.join(EVIL_DIR, fname)
        result = subprocess.run(["python3", CLASSIFIER_SCRIPT, fpath], capture_output=True)
        if result.returncode == 0:
            failed_files.append(fname)

    if failed_files:
        pytest.fail(
            f"{len(failed_files)} of {len(evil_files)} evil bypassed (expected exit > 0). "
            f"Offending files: {', '.join(failed_files)}"
        )