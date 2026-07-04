# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/classifier.sh"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_script_exists_and_executable():
    """Test that the classifier script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Classifier script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Classifier script at {SCRIPT_PATH} is not executable"

def test_adversarial_corpus():
    """Test the classifier against the evil and clean corpora."""
    if not os.path.isfile(SCRIPT_PATH) or not os.access(SCRIPT_PATH, os.X_OK):
        pytest.fail("Classifier script missing or not executable.")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, "Evil corpus is empty."
    assert len(clean_files) > 0, "Clean corpus is empty."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run([SCRIPT_PATH, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run([SCRIPT_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:10])}{'...' if len(evil_bypassed) > 10 else ''}")

    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified[:10])}{'...' if len(clean_modified) > 10 else ''}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))