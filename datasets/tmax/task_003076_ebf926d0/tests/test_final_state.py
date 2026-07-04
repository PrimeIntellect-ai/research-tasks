# test_final_state.py
import os
import subprocess
import pytest

BINARY_PATH = "/home/user/log_checker"
CLEAN_CORPUS = "/app/corpora/clean"
EVIL_CORPUS = "/app/corpora/evil"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Binary {BINARY_PATH} does not exist. The tool was not compiled to the correct location."
    assert os.access(BINARY_PATH, os.X_OK), f"Binary {BINARY_PATH} is not executable."

def test_clean_corpus():
    if not os.path.isfile(BINARY_PATH):
        pytest.skip("Binary not found")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    failed_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS, filename)
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True, text=True)
        # Clean files should exit 0 and output CLEAN
        if result.returncode != 0 or "CLEAN" not in result.stdout.upper():
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}"

def test_evil_corpus():
    if not os.path.isfile(BINARY_PATH):
        pytest.skip("Binary not found")

    evil_files = [f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    failed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS, filename)
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True, text=True)
        # Evil files should exit 1 and output EVIL
        if result.returncode != 1 or "EVIL" not in result.stdout.upper():
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}"