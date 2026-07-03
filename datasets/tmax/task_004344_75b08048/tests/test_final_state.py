# test_final_state.py

import os
import subprocess
import pytest

EVIL_DIR = "/verify/evil"
CLEAN_DIR = "/verify/clean"
SCRIPT_PATH = "/home/user/sanitizer.py"

def run_sanitizer(query_content: str) -> str:
    result = subprocess.run(
        ["python3", SCRIPT_PATH, query_content],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def test_sanitizer_exists():
    assert os.path.exists(SCRIPT_PATH), f"Sanitizer script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_evil_corpus_rejected():
    assert os.path.exists(EVIL_DIR), f"Evil corpus directory {EVIL_DIR} not found"

    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus"

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        with open(filepath, 'r') as f:
            query = f.read().strip()

        output = run_sanitizer(query)
        if output != "REJECT":
            failed_files.append((filename, output))

    if failed_files:
        details = ", ".join([f"{f} (output: {out})" for f, out in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil queries bypassed: {details}")

def test_clean_corpus_accepted():
    assert os.path.exists(CLEAN_DIR), f"Clean corpus directory {CLEAN_DIR} not found"

    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus"

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        with open(filepath, 'r') as f:
            query = f.read().strip()

        output = run_sanitizer(query)
        if output != "ACCEPT":
            failed_files.append((filename, output))

    if failed_files:
        details = ", ".join([f"{f} (output: {out})" for f, out in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean queries modified/rejected: {details}")