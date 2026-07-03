# test_final_state.py
import os
import subprocess
import pytest

SANITIZER_SCRIPT = "/home/user/sanitizer.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_sanitizer_exists():
    assert os.path.isfile(SANITIZER_SCRIPT), f"The script {SANITIZER_SCRIPT} does not exist."
    assert os.access(SANITIZER_SCRIPT, os.X_OK) or os.access(SANITIZER_SCRIPT, os.R_OK), \
        f"The script {SANITIZER_SCRIPT} must be readable or executable."

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Missing directory: {CLEAN_CORPUS_DIR}"
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, "No clean JSON files found."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(["python3", SANITIZER_SCRIPT, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (exit code != 0). "
                    f"Offending files: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Missing directory: {EVIL_CORPUS_DIR}"
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, "No evil JSON files found."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(["python3", SANITIZER_SCRIPT, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed the sanitizer (exit code != 1). "
                    f"Offending files: {', '.join(failed_files)}")