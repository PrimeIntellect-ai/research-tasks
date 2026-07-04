# test_final_state.py

import os
import subprocess
import pytest
from concurrent.futures import ThreadPoolExecutor

SCANNER_PATH = "/home/user/scanner"
LOG_PATH = "/home/user/artifact_log.txt"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_scanner_exists():
    assert os.path.isfile(SCANNER_PATH), f"Scanner binary not found at {SCANNER_PATH}"
    assert os.access(SCANNER_PATH, os.X_OK), f"Scanner at {SCANNER_PATH} is not executable"

def test_adversarial_corpus_and_logging():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus directory missing at {CLEAN_CORPUS}"
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus directory missing at {EVIL_CORPUS}"

    clean_files = sorted([os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if f.endswith('.gz')])
    evil_files = sorted([os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if f.endswith('.gz')])

    # Remove log file if it exists from manual testing to ensure a clean slate for the concurrent test
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    clean_failed = []
    evil_failed = []

    def run_scanner(filepath):
        result = subprocess.run([SCANNER_PATH, filepath], capture_output=True)
        return filepath, result.returncode

    # Run concurrently to test POSIX locking and performance
    with ThreadPoolExecutor(max_workers=20) as executor:
        clean_results = list(executor.map(run_scanner, clean_files))
        evil_results = list(executor.map(run_scanner, evil_files))

    for filepath, code in clean_results:
        if code != 0:
            clean_failed.append(os.path.basename(filepath))

    for filepath, code in evil_results:
        if code != 1:
            evil_failed.append(os.path.basename(filepath))

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

    # Validate log file contents and locking (no corrupted lines)
    assert os.path.isfile(LOG_PATH), f"Log file not found at {LOG_PATH}"
    with open(LOG_PATH, 'r') as f:
        lines = f.read().splitlines()

    expected_entries = set()
    for filepath in clean_files:
        expected_entries.add(f"{os.path.basename(filepath)} - CLEAN")
    for filepath in evil_files:
        expected_entries.add(f"{os.path.basename(filepath)} - REJECTED")

    actual_entries = set(lines)

    missing_entries = expected_entries - actual_entries
    assert not missing_entries, f"Missing expected log entries: {missing_entries}"

    # Check for corrupted lines (lines that don't match expected format)
    for line in lines:
        assert line in expected_entries, f"Unexpected or corrupted log entry found: '{line}'"