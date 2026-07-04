# test_final_state.py

import os
import subprocess
import pytest

FILTER_BIN = "/home/user/filter"
EVAL_CLEAN_DIR = "/eval/corpus/clean"
EVAL_EVIL_DIR = "/eval/corpus/evil"

def test_filter_executable_exists():
    assert os.path.isfile(FILTER_BIN), f"Filter binary not found at {FILTER_BIN}"
    assert os.access(FILTER_BIN, os.X_OK), f"Filter binary at {FILTER_BIN} is not executable"

def test_filter_clean_corpus():
    assert os.path.isdir(EVAL_CLEAN_DIR), f"Clean eval corpus missing at {EVAL_CLEAN_DIR}"
    clean_files = [os.path.join(EVAL_CLEAN_DIR, f) for f in os.listdir(EVAL_CLEAN_DIR) if os.path.isfile(os.path.join(EVAL_CLEAN_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean eval corpus"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([FILTER_BIN, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (exit code != 0): {', '.join(failed_files)}")

def test_filter_evil_corpus():
    assert os.path.isdir(EVAL_EVIL_DIR), f"Evil eval corpus missing at {EVAL_EVIL_DIR}"
    evil_files = [os.path.join(EVAL_EVIL_DIR, f) for f in os.listdir(EVAL_EVIL_DIR) if os.path.isfile(os.path.join(EVAL_EVIL_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil eval corpus"

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run([FILTER_BIN, filepath], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed the filter (exit code == 0): {', '.join(bypassed_files)}")