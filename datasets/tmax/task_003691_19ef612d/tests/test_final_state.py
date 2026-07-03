# test_final_state.py

import os
import subprocess
import pytest

CLASSIFIER_SCRIPT = "/home/user/classifier.sh"
EVIL_CORPUS_DIR = "/app/corpora/evil/"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"

def test_classifier_script_exists():
    assert os.path.isfile(CLASSIFIER_SCRIPT), f"Classifier script is missing at {CLASSIFIER_SCRIPT}"
    assert os.access(CLASSIFIER_SCRIPT, os.X_OK) or os.access(CLASSIFIER_SCRIPT, os.R_OK), f"Classifier script at {CLASSIFIER_SCRIPT} is not readable/executable"

def test_evil_corpus_classification():
    if not os.path.isfile(CLASSIFIER_SCRIPT):
        pytest.fail(f"Classifier script missing at {CLASSIFIER_SCRIPT}")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, f"No files found in evil corpus at {EVIL_CORPUS_DIR}"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(["bash", CLASSIFIER_SCRIPT, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed the classifier (expected exit code 1). Offending files: {', '.join(failed_files)}")

def test_clean_corpus_classification():
    if not os.path.isfile(CLASSIFIER_SCRIPT):
        pytest.fail(f"Classifier script missing at {CLASSIFIER_SCRIPT}")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, f"No files found in clean corpus at {CLEAN_CORPUS_DIR}"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(["bash", CLASSIFIER_SCRIPT, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly flagged (expected exit code 0). Offending files: {', '.join(failed_files)}")