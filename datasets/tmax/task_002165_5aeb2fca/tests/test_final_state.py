# test_final_state.py

import os
import subprocess
import pytest

SANITIZER_PATH = "/home/user/sanitizer.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_sanitizer_exists():
    assert os.path.isfile(SANITIZER_PATH), f"Sanitizer script not found at {SANITIZER_PATH}"

def test_sanitizer_clean_corpus():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.fail(f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    if not clean_files:
        pytest.fail(f"No JSON files found in clean corpus: {CLEAN_CORPUS_DIR}")

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(
            ["python3", SANITIZER_PATH, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (exit code != 0). Offending files: {', '.join(failed_files)}")

def test_sanitizer_evil_corpus():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.fail(f"Evil corpus directory missing: {EVIL_CORPUS_DIR}")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    if not evil_files:
        pytest.fail(f"No JSON files found in evil corpus: {EVIL_CORPUS_DIR}")

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(
            ["python3", SANITIZER_PATH, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed the sanitizer (exit code != 1). Offending files: {', '.join(failed_files)}")