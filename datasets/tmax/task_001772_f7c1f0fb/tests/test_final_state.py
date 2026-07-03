# test_final_state.py

import os
import subprocess
import pytest

CLASSIFIER_PATH = "/home/user/classifier/target/release/classifier"
CLEAN_CORPUS_DIR = "/app/eval_corpora/clean"
EVIL_CORPUS_DIR = "/app/eval_corpora/evil"

def test_classifier_binary_exists():
    assert os.path.exists(CLASSIFIER_PATH), f"Classifier binary not found at {CLASSIFIER_PATH}. Did you compile it in release mode?"
    assert os.path.isfile(CLASSIFIER_PATH), f"Path {CLASSIFIER_PATH} is not a file."
    assert os.access(CLASSIFIER_PATH, os.X_OK), f"Classifier binary at {CLASSIFIER_PATH} is not executable."

def run_classifier(file_path):
    result = subprocess.run(
        [CLASSIFIER_PATH, file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.returncode

def test_clean_corpus():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus directory {CLEAN_CORPUS_DIR} is missing."
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, f"No JSON files found in clean corpus directory {CLEAN_CORPUS_DIR}."

    failed_files = []
    for f in clean_files:
        if run_classifier(f) != 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (modified/flagged). Offending files: {failed_files}")

def test_evil_corpus():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus directory {EVIL_CORPUS_DIR} is missing."
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, f"No JSON files found in evil corpus directory {EVIL_CORPUS_DIR}."

    failed_files = []
    for f in evil_files:
        if run_classifier(f) == 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed detection. Offending files: {failed_files}")