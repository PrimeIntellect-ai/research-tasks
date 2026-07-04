# test_final_state.py

import os
import subprocess
import pytest

EVIL_CORPUS_DIR = "/app/data/corpus/evil/"
CLEAN_CORPUS_DIR = "/app/data/corpus/clean/"
SCRIPT_PATH = "/home/user/pipeline/archive_filter.py"

def run_script(file_path):
    cmd = ["python3", SCRIPT_PATH, "process", file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip()

def test_evil_corpus_rejected():
    if not os.path.exists(EVIL_CORPUS_DIR):
        pytest.skip(f"Evil corpus directory not found: {EVIL_CORPUS_DIR}")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    if not evil_files:
        pytest.skip("No files found in evil corpus.")

    bypassed = []
    for filepath in evil_files:
        code, stdout = run_script(filepath)
        if code != 1 or "REJECTED" not in stdout:
            bypassed.append(os.path.basename(filepath))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")

def test_clean_corpus_accepted():
    if not os.path.exists(CLEAN_CORPUS_DIR):
        pytest.skip(f"Clean corpus directory not found: {CLEAN_CORPUS_DIR}")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    if not clean_files:
        pytest.skip("No files found in clean corpus.")

    modified = []
    for filepath in clean_files:
        code, stdout = run_script(filepath)
        if code != 0 or "ACCEPTED" not in stdout:
            modified.append(os.path.basename(filepath))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/rejected: {', '.join(modified)}")