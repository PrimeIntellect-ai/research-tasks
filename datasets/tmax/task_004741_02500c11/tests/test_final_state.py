# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/payload_filter.sh"
CLEAN_CORPUS = "/app/corpus/clean/"
EVIL_CORPUS = "/app/corpus/evil/"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_adversarial_corpus_evaluation():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus directory missing: {CLEAN_CORPUS}"
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus directory missing: {EVIL_CORPUS}"

    clean_files = sorted([f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))])
    evil_files = sorted([f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))])

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    clean_rejected = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS, filename)
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(filename)

    evil_bypassed = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS, filename)
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(filename)

    errors = []
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_rejected)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))