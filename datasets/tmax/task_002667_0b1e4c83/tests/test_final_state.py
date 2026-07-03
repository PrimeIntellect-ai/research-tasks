# test_final_state.py

import os
import subprocess
import glob
import pytest

SCRIPT_PATH = "/home/user/sanitize_loc.py"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"

def test_clean_corpus_accepted():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    assert clean_files, f"No clean corpus files found in {CLEAN_CORPUS_DIR}"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))
    assert evil_files, f"No evil corpus files found in {EVIL_CORPUS_DIR}"

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed: {', '.join(bypassed_files)}")