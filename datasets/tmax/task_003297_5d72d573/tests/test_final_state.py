# test_final_state.py

import os
import subprocess
import pytest
import glob

SCRIPT_PATH = "/home/user/evaluate_graph.py"
CLEAN_CORPUS_DIR = "/home/user/corpus/clean"
EVIL_CORPUS_DIR = "/home/user/corpus/evil"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"The required script was not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"The path {SCRIPT_PATH} is not a valid file"

def test_clean_corpus_accepted():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))
    assert len(clean_files) > 0, f"No JSON files found in the clean corpus directory at {CLEAN_CORPUS_DIR}."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, filepath], capture_output=True, text=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))
    assert len(evil_files) > 0, f"No JSON files found in the evil corpus directory at {EVIL_CORPUS_DIR}."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, filepath], capture_output=True, text=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}")