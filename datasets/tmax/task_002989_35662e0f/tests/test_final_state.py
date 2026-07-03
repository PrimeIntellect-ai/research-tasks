# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/threat_filter.sh"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a regular file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"The script {SCRIPT_PATH} is not executable. Did you run 'chmod +x'?"

def test_adversarial_corpus_evaluation():
    if not os.path.exists(SCRIPT_PATH) or not os.access(SCRIPT_PATH, os.X_OK):
        pytest.fail(f"Cannot run tests because {SCRIPT_PATH} is missing or not executable.")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    bypassed_evil = []
    modified_clean = []

    # Test evil corpus
    for filepath in evil_files:
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(filepath))

    # Test clean corpus
    for filepath in clean_files:
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            modified_clean.append(os.path.basename(filepath))

    error_messages = []
    if bypassed_evil:
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_messages.append(f"{len(modified_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(modified_clean)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))