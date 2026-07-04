# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sanitizer.py"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"

def test_sanitizer_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Sanitizer script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_adversarial_corpus():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus (expected to exit 1)
    for evil_file in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    # Test clean corpus (expected to exit 0)
    for clean_file in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))