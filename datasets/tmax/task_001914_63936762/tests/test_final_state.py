# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/validate_telemetry.sh"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def run_script_with_url(url):
    """Runs the script with the given URL and returns the exit code."""
    result = subprocess.run([SCRIPT_PATH, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode

def test_clean_corpus():
    """Asserts that all clean URLs are accepted (exit code 0)."""
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus directory missing at {CLEAN_CORPUS_DIR}"

    failed_files = []
    total_files = 0

    for filename in sorted(os.listdir(CLEAN_CORPUS_DIR)):
        file_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, 'r') as f:
            url = f.read().strip()

        total_files += 1
        exit_code = run_script_with_url(url)

        if exit_code != 0:
            failed_files.append((filename, url, exit_code))

    if failed_files:
        error_msg = f"{len(failed_files)} of {total_files} clean modified/rejected.\nOffending files:\n"
        for fname, url, code in failed_files:
            error_msg += f"  - {fname} (exit code {code}) for URL: {url}\n"
        pytest.fail(error_msg)

def test_evil_corpus():
    """Asserts that all evil URLs are rejected (exit code 1)."""
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus directory missing at {EVIL_CORPUS_DIR}"

    failed_files = []
    total_files = 0

    for filename in sorted(os.listdir(EVIL_CORPUS_DIR)):
        file_path = os.path.join(EVIL_CORPUS_DIR, filename)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, 'r') as f:
            url = f.read().strip()

        total_files += 1
        exit_code = run_script_with_url(url)

        if exit_code == 0:
            failed_files.append((filename, url, exit_code))

    if failed_files:
        error_msg = f"{len(failed_files)} of {total_files} evil bypassed/accepted.\nOffending files:\n"
        for fname, url, code in failed_files:
            error_msg += f"  - {fname} (exit code {code}) for URL: {url}\n"
        pytest.fail(error_msg)