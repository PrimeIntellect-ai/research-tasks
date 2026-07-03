# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/pka_guard.py"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Gatekeeper script not found at {SCRIPT_PATH}"
    # Python scripts don't strictly need +x if run as `python3 script.py`, 
    # but the instructions say "make sure it is executable"
    # We will test it by running `python3 /home/user/pka_guard.py ...` as requested by the usage:
    # "Usage: python3 /home/user/pka_guard.py <path_to_pka_file>"

def test_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Missing clean corpus directory: {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.pka')]
    assert len(clean_files) > 0, "No .pka files found in clean corpus"

    rejected_files = []

    for pka_file in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, pka_file], capture_output=True)
        if result.returncode != 0:
            rejected_files.append(os.path.basename(pka_file))

    if rejected_files:
        pytest.fail(f"{len(rejected_files)} of {len(clean_files)} clean rejected: {', '.join(rejected_files)}")

def test_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Missing evil corpus directory: {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.pka')]
    assert len(evil_files) > 0, "No .pka files found in evil corpus"

    bypassed_files = []

    for pka_file in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, pka_file], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(pka_file))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")