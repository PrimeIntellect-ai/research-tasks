# test_final_state.py

import os
import subprocess
import pytest

VERIFIER_PATH = "/home/user/verifier"
EVIL_CORPUS_DIR = "/home/user/corpus/evil"
CLEAN_CORPUS_DIR = "/home/user/corpus/clean"

def test_verifier_exists_and_executable():
    assert os.path.isfile(VERIFIER_PATH), f"Verifier executable not found at {VERIFIER_PATH}"
    assert os.access(VERIFIER_PATH, os.X_OK), f"Verifier at {VERIFIER_PATH} is not executable"

def test_verifier_adversarial_corpus():
    if not os.path.isfile(VERIFIER_PATH) or not os.access(VERIFIER_PATH, os.X_OK):
        pytest.fail("Verifier executable is missing or not executable.")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    for evil_file in evil_files:
        file_path = os.path.join(EVIL_CORPUS_DIR, evil_file)
        result = subprocess.run([VERIFIER_PATH, file_path], capture_output=True, text=True)

        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "REJECT":
            evil_bypassed.append((evil_file, result.returncode, stdout))

    clean_rejected = []
    for clean_file in clean_files:
        file_path = os.path.join(CLEAN_CORPUS_DIR, clean_file)
        result = subprocess.run([VERIFIER_PATH, file_path], capture_output=True, text=True)

        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "ACCEPT":
            clean_rejected.append((clean_file, result.returncode, stdout))

    error_messages = []
    if evil_bypassed:
        bypassed_names = [x[0] for x in evil_bypassed]
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {bypassed_names}")

    if clean_rejected:
        rejected_names = [x[0] for x in clean_rejected]
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified/rejected: {rejected_names}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))