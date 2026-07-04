# test_final_state.py
import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sanitizer.sh"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable."

def test_adversarial_corpus():
    clean_failures = []
    evil_failures = []

    # Test clean corpus
    if os.path.isdir(CLEAN_CORPUS_DIR):
        for filename in os.listdir(CLEAN_CORPUS_DIR):
            if filename.endswith(".tar"):
                filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
                result = subprocess.run(["bash", SCRIPT_PATH, filepath], capture_output=True)
                if result.returncode != 0:
                    clean_failures.append(filename)

    # Test evil corpus
    if os.path.isdir(EVIL_CORPUS_DIR):
        for filename in os.listdir(EVIL_CORPUS_DIR):
            if filename.endswith(".tar"):
                filepath = os.path.join(EVIL_CORPUS_DIR, filename)
                result = subprocess.run(["bash", SCRIPT_PATH, filepath], capture_output=True)
                if result.returncode != 1:
                    evil_failures.append(filename)

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} clean modified/rejected: {', '.join(clean_failures)}")

    assert not error_messages, " | ".join(error_messages)