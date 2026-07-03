# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/detector.sh"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_adversarial_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*"))
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*"))

    assert len(evil_files) > 0, "No files found in evil corpus directory."
    assert len(clean_files) > 0, "No files found in clean corpus directory."

    evil_bypassed = []
    for filepath in evil_files:
        if not os.path.isfile(filepath):
            continue
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        # Evil files should be rejected (exit code 1)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(filepath))

    clean_modified = []
    for filepath in clean_files:
        if not os.path.isfile(filepath):
            continue
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        # Clean files should be preserved (exit code 0)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(filepath))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:5])}{'...' if len(evil_bypassed) > 5 else ''}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified[:5])}{'...' if len(clean_modified) > 5 else ''}")

    assert not error_messages, " | ".join(error_messages)