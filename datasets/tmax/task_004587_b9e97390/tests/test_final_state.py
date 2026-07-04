# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sanitizer.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_sanitizer_exists():
    """Ensure the user created the sanitizer script."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_adversarial_corpus():
    """Test the sanitizer script against the clean and evil corpora."""
    assert os.path.exists(CLEAN_CORPUS_DIR), "Clean corpus directory missing."
    assert os.path.exists(EVIL_CORPUS_DIR), "Evil corpus directory missing."

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]

    assert clean_files, "No clean corpus files found."
    assert evil_files, "No evil corpus files found."

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, ef], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean files modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil files bypassed: {', '.join(evil_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))