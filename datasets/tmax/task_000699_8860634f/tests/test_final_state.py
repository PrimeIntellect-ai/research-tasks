# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/ws_server/sanitize"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_binary_exists_and_executable():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def test_adversarial_corpus_evil():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.fail(f"Evil corpus directory missing: {EVIL_CORPUS_DIR}")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed_files = []

    for file_path in evil_files:
        result = subprocess.run([BINARY_PATH, file_path], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(file_path))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil payloads bypassed: {', '.join(bypassed_files)}")

def test_adversarial_corpus_clean():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.fail(f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No clean corpus files found."

    modified_files = []

    for file_path in clean_files:
        with open(file_path, "rb") as f:
            expected_content = f.read()

        result = subprocess.run([BINARY_PATH, file_path], capture_output=True)

        if result.returncode != 0 or result.stdout != expected_content:
            modified_files.append(os.path.basename(file_path))

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean payloads modified or rejected: {', '.join(modified_files)}")