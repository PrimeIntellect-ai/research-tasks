# test_final_state.py

import os
import subprocess
import pytest

CLASSIFIER_PATH = "/home/user/classifier"
EVIL_CORPUS_DIR = "/home/user/evidence/evil/"
CLEAN_CORPUS_DIR = "/home/user/evidence/clean/"

def test_classifier_exists_and_executable():
    assert os.path.exists(CLASSIFIER_PATH), f"Classifier binary not found at {CLASSIFIER_PATH}"
    assert os.path.isfile(CLASSIFIER_PATH), f"Classifier path {CLASSIFIER_PATH} is not a file"
    assert os.access(CLASSIFIER_PATH, os.X_OK), f"Classifier binary at {CLASSIFIER_PATH} is not executable"

def test_classifier_against_adversarial_corpus():
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, f"No files found in evil corpus directory {EVIL_CORPUS_DIR}"
    assert len(clean_files) > 0, f"No files found in clean corpus directory {CLEAN_CORPUS_DIR}"

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run([CLASSIFIER_PATH, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run([CLASSIFIER_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:10])}{'...' if len(evil_bypassed) > 10 else ''}")

    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified[:10])}{'...' if len(clean_modified) > 10 else ''}")

    assert not error_messages, " | ".join(error_messages)