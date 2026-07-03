# test_final_state.py

import os
import subprocess
import pytest

FILTER_SCRIPT = "/home/user/filter.py"
EVIL_CORPUS_DIR = "/app/test_corpus/evil/"
CLEAN_CORPUS_DIR = "/app/test_corpus/clean/"

def test_filter_script_exists():
    assert os.path.exists(FILTER_SCRIPT), f"Missing script at {FILTER_SCRIPT}"
    assert os.path.isfile(FILTER_SCRIPT), f"{FILTER_SCRIPT} is not a file"

def run_filter(csv_path):
    result = subprocess.run(
        ["python3", FILTER_SCRIPT, csv_path],
        capture_output=True,
        text=True,
        timeout=5
    )
    return result.stdout.strip()

def test_evil_corpus():
    assert os.path.exists(EVIL_CORPUS_DIR), "Evil corpus directory missing"
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]
    assert len(evil_files) > 0, "No CSV files in evil corpus"

    bypassed = []
    for f in evil_files:
        path = os.path.join(EVIL_CORPUS_DIR, f)
        output = run_filter(path)
        if output != "EVIL":
            bypassed.append((f, output))

    if bypassed:
        details = ", ".join([f"{f} (output: {out})" for f, out in bypassed])
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {details}")

def test_clean_corpus():
    assert os.path.exists(CLEAN_CORPUS_DIR), "Clean corpus directory missing"
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    assert len(clean_files) > 0, "No CSV files in clean corpus"

    modified = []
    for f in clean_files:
        path = os.path.join(CLEAN_CORPUS_DIR, f)
        output = run_filter(path)
        if output != "CLEAN":
            modified.append((f, output))

    if modified:
        details = ", ".join([f"{f} (output: {out})" for f, out in modified])
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified: {details}")