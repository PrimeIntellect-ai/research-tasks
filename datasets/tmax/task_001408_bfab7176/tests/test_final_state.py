# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/query_sanitizer/target/release/query_sanitizer"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"
EVIL_CORPUS_DIR = "/app/corpora/evil/"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Expected compiled Rust binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def run_sanitizer(file_path):
    try:
        result = subprocess.run(
            [BINARY_PATH, file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_clean_corpus():
    if not os.path.isfile(BINARY_PATH):
        pytest.skip("Binary not found")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, f"No JSON files found in clean corpus dir: {CLEAN_CORPUS_DIR}"

    failed_files = []
    for filename in clean_files:
        file_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        output = run_sanitizer(file_path)
        if output != "ACCEPT":
            failed_files.append((filename, output))

    if failed_files:
        details = ", ".join([f"{name} (got {out})" for name, out in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected or failed: {details}")

def test_evil_corpus():
    if not os.path.isfile(BINARY_PATH):
        pytest.skip("Binary not found")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, f"No JSON files found in evil corpus dir: {EVIL_CORPUS_DIR}"

    failed_files = []
    for filename in evil_files:
        file_path = os.path.join(EVIL_CORPUS_DIR, filename)
        output = run_sanitizer(file_path)
        if output != "REJECT":
            failed_files.append((filename, output))

    if failed_files:
        details = ", ".join([f"{name} (got {out})" for name, out in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed or failed: {details}")