# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/evaluate_sample.py"
CLEAN_CORPUS_DIR = "/app/eval_corpus/clean/"
EVIL_CORPUS_DIR = "/app/eval_corpus/evil/"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing at {CLEAN_CORPUS_DIR}"
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".csv")]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for f in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files rejected (should be accepted): {failed_files}"

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing at {EVIL_CORPUS_DIR}"
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".csv")]
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for f in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, f], capture_output=True)
        # Evil files must be rejected (exit code != 0)
        if result.returncode == 0:
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed/accepted (should be rejected): {failed_files}"