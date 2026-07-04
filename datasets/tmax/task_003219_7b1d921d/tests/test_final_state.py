# test_final_state.py

import os
import subprocess
import pytest

CLASSIFIER_PATH = "/home/user/classifier.py"
EVIL_CORPUS_DIR = "/app/corpora/evil/"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"

def test_classifier_exists():
    assert os.path.isfile(CLASSIFIER_PATH), f"Classifier script not found at {CLASSIFIER_PATH}"

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, f"No JSON files found in {EVIL_CORPUS_DIR}"

    bypassed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run(["python3", CLASSIFIER_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil payloads bypassed validation (expected exit code 1): {', '.join(bypassed_files)}")

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, f"No JSON files found in {CLEAN_CORPUS_DIR}"

    modified_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run(["python3", CLASSIFIER_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            modified_files.append(filename)

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean payloads were rejected (expected exit code 0): {', '.join(modified_files)}")