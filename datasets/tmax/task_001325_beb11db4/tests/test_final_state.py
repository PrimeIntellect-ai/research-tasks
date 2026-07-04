# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/query_sanitizer/target/release/query_sanitizer"
CLEAN_CORPUS_DIR = "/app/test_corpora/clean"
EVIL_CORPUS_DIR = "/app/test_corpora/evil"

def test_sanitizer_binary_exists():
    assert os.path.exists(BINARY_PATH), f"Sanitizer binary not found at {BINARY_PATH}"
    assert os.path.isfile(BINARY_PATH), f"Sanitizer path {BINARY_PATH} is not a file"
    assert os.access(BINARY_PATH, os.X_OK), f"Sanitizer binary {BINARY_PATH} is not executable"

def test_adversarial_corpus():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]

    assert clean_files, "No clean files found in corpus"
    assert evil_files, "No evil files found in corpus"

    clean_failed = []
    evil_failed = []

    for clean_file in clean_files:
        try:
            result = subprocess.run([BINARY_PATH, clean_file], capture_output=True, text=True, timeout=5)
            if result.returncode != 0 or "SAFE" not in result.stdout:
                clean_failed.append(os.path.basename(clean_file))
        except Exception as e:
            clean_failed.append(os.path.basename(clean_file))

    for evil_file in evil_files:
        try:
            result = subprocess.run([BINARY_PATH, evil_file], capture_output=True, text=True, timeout=5)
            if result.returncode != 1 or "EVIL" not in result.stdout:
                evil_failed.append(os.path.basename(evil_file))
        except Exception as e:
            # If it errors out differently, it's not correctly handled
            evil_failed.append(os.path.basename(evil_file))

    error_messages = []
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))