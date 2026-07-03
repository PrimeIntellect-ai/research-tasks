# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/spam_filter.py"
EVIL_CORPUS_DIR = "/app/eval_evil/"
CLEAN_CORPUS_DIR = "/app/eval_clean/"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory not found at {EVIL_CORPUS_DIR}"
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus"

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run(["python", SCRIPT_PATH, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "EVIL":
            failed_files.append((filename, output))

    if failed_files:
        details = ", ".join([f"{f} (output: {out})" for f, out in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed. Failed files: {details}")

def test_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory not found at {CLEAN_CORPUS_DIR}"
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus"

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run(["python", SCRIPT_PATH, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "CLEAN":
            failed_files.append((filename, output))

    if failed_files:
        details = ", ".join([f"{f} (output: {out})" for f, out in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/flagged. Failed files: {details}")