# test_final_state.py

import os
import subprocess
import pytest

CLASSIFIER_PATH = '/home/user/classifier'
CLEAN_CORPUS_DIR = '/test/clean'
EVIL_CORPUS_DIR = '/test/evil'

def test_classifier_exists_and_executable():
    """Check that the compiled classifier exists and is executable."""
    assert os.path.isfile(CLASSIFIER_PATH), f"Classifier binary missing at {CLASSIFIER_PATH}"
    assert os.access(CLASSIFIER_PATH, os.X_OK), f"Classifier binary at {CLASSIFIER_PATH} is not executable"

def test_adversarial_corpus():
    """Run the classifier against the clean and evil corpora."""
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus missing at {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus missing at {EVIL_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    clean_failed = []
    for filepath in clean_files:
        result = subprocess.run([CLASSIFIER_PATH, filepath], capture_output=True, text=True)
        # Clean should have exit code 0
        if result.returncode != 0:
            clean_failed.append(os.path.basename(filepath))

    evil_bypassed = []
    for filepath in evil_files:
        result = subprocess.run([CLASSIFIER_PATH, filepath], capture_output=True, text=True)
        # Evil should have exit code 1
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(filepath))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not errors, " | ".join(errors)