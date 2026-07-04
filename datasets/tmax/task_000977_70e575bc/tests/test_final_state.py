# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/wal_classifier.sh"
CLEAN_CORPUS_DIR = "/app/hidden_corpus/clean/"
EVIL_CORPUS_DIR = "/app/hidden_corpus/evil/"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_adversarial_corpus_classification():
    if not os.path.exists(SCRIPT_PATH) or not os.access(SCRIPT_PATH, os.X_OK):
        pytest.fail(f"Cannot run test, valid executable script missing at {SCRIPT_PATH}")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    clean_misclassified = []
    for cf in clean_files:
        result = subprocess.run([SCRIPT_PATH, cf], capture_output=True)
        if result.returncode != 0:
            clean_misclassified.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        result = subprocess.run([SCRIPT_PATH, ef], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:5])}{'...' if len(evil_bypassed) > 5 else ''}")
    if clean_misclassified:
        errors.append(f"{len(clean_misclassified)} of {len(clean_files)} clean modified (misclassified): {', '.join(clean_misclassified[:5])}{'...' if len(clean_misclassified) > 5 else ''}")

    if errors:
        pytest.fail(" | ".join(errors))