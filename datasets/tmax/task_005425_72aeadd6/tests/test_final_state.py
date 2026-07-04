# test_final_state.py
import os
import subprocess
import pytest

BINARY_PATH = "/home/user/log_sanitizer/sanitizer"
CLEAN_CORPUS_DIR = "/home/user/log_sanitizer/corpus/clean"
EVIL_CORPUS_DIR = "/home/user/log_sanitizer/corpus/evil"
TIMEOUT = 2.0  # seconds

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"File at {BINARY_PATH} is not executable"

def test_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory."

    failed_files = []
    for filepath in clean_files:
        try:
            result = subprocess.run([BINARY_PATH, filepath], capture_output=True, timeout=TIMEOUT)
            if result.returncode != 0:
                failed_files.append(os.path.basename(filepath))
        except subprocess.TimeoutExpired:
            failed_files.append(f"{os.path.basename(filepath)} (timeout)")
        except Exception as e:
            failed_files.append(f"{os.path.basename(filepath)} (error: {e})")

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean logs modified/rejected: {', '.join(failed_files)}")

def test_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    failed_files = []
    for filepath in evil_files:
        try:
            result = subprocess.run([BINARY_PATH, filepath], capture_output=True, timeout=TIMEOUT)
            if result.returncode != 1:
                failed_files.append(os.path.basename(filepath))
        except subprocess.TimeoutExpired:
            failed_files.append(f"{os.path.basename(filepath)} (timeout)")
        except Exception as e:
            failed_files.append(f"{os.path.basename(filepath)} (error: {e})")

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil logs bypassed/accepted: {', '.join(failed_files)}")