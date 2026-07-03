# test_final_state.py

import os
import subprocess
import pytest

FILTER_SCRIPT = "/home/user/filter.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_filter_script_exists():
    assert os.path.exists(FILTER_SCRIPT), f"Filter script not found at {FILTER_SCRIPT}"
    assert os.path.isfile(FILTER_SCRIPT), f"Path is not a file: {FILTER_SCRIPT}"

def test_clean_corpus_accepted():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "Clean corpus is empty"

    rejected_files = []

    for file_path in clean_files:
        result = subprocess.run(["python3", FILTER_SCRIPT, file_path], capture_output=True)
        if result.returncode != 0:
            rejected_files.append(os.path.basename(file_path))

    if rejected_files:
        pytest.fail(f"{len(rejected_files)} of {len(clean_files)} clean rejected: {', '.join(rejected_files)}")

def test_evil_corpus_rejected():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "Evil corpus is empty"

    bypassed_files = []

    for file_path in evil_files:
        result = subprocess.run(["python3", FILTER_SCRIPT, file_path], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(file_path))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")