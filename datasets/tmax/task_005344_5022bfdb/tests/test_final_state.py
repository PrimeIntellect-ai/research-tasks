# test_final_state.py

import os
import subprocess
import glob
import pytest

SCRIPT_PATH = "/home/user/filter_archive.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*"))
    assert len(clean_files) > 0, "No clean corpus files found."

    rejected = []
    for filepath in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            rejected.append(os.path.basename(filepath))

    if rejected:
        pytest.fail(f"{len(rejected)} of {len(clean_files)} clean rejected: {', '.join(rejected)}")

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*"))
    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed = []
    for filepath in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode == 0:
            bypassed.append(os.path.basename(filepath))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")