# test_final_state.py

import os
import subprocess
import pytest

SCANNER_PATH = "/home/user/scan_corpus/scanner"
EVIL_CORPUS_DIR = "/home/user/corpus/evil"
CLEAN_CORPUS_DIR = "/home/user/corpus/clean"

def run_scanner(corpus_dir):
    assert os.path.isfile(SCANNER_PATH), f"Scanner executable not found at {SCANNER_PATH}"
    assert os.access(SCANNER_PATH, os.X_OK), f"Scanner at {SCANNER_PATH} is not executable"

    try:
        result = subprocess.run(
            [SCANNER_PATH, corpus_dir],
            capture_output=True,
            text=True,
            timeout=10,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Scanner crashed or failed when running on {corpus_dir} (possibly due to unfixed C code or gRPC server not running). stderr: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Scanner timed out when running on {corpus_dir}")

def test_evil_corpus_rejected():
    """
    Iterate over every file in the evil corpus path and assert the agent's solution rejects each one.
    """
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing at {EVIL_CORPUS_DIR}"
    stdout = run_scanner(EVIL_CORPUS_DIR)

    files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    bypassed = []

    for filename in files:
        expected_line = f"{filename}: REJECTED"
        if expected_line not in stdout:
            bypassed.append(filename)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(files)} evil bypassed: {', '.join(bypassed)}")

def test_clean_corpus_accepted():
    """
    Iterate over every file in the clean corpus path and assert the agent's solution accepts each one.
    """
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing at {CLEAN_CORPUS_DIR}"
    stdout = run_scanner(CLEAN_CORPUS_DIR)

    files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    modified = []

    for filename in files:
        expected_line = f"{filename}: ACCEPTED"
        if expected_line not in stdout:
            modified.append(filename)

    if modified:
        pytest.fail(f"{len(modified)} of {len(files)} clean modified: {', '.join(modified)}")