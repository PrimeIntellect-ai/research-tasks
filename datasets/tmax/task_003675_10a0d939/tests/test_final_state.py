# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/filter_logs.py"
EVIL_CORPUS_DIR = "/app/corpora/evil"
CLEAN_CORPUS_DIR = "/app/corpora/clean"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file."

def run_filter_script(input_csv_path):
    result = subprocess.run(
        ["python3", SCRIPT_PATH, input_csv_path],
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr

def test_evil_corpus_rejected():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Directory {EVIL_CORPUS_DIR} does not exist."
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]
    assert len(evil_files) > 0, f"No CSV files found in {EVIL_CORPUS_DIR}."

    bypassed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        returncode, stdout, stderr = run_filter_script(filepath)

        if returncode != 0:
            bypassed_files.append((filename, f"Script exited with code {returncode}"))
            continue

        lines = stdout.strip().split('\n')
        # Should only contain the header
        if len(lines) > 1:
            bypassed_files.append((filename, f"Failed to reject {len(lines)-1} evil rows"))

    if bypassed_files:
        details = ", ".join([f"{f}: {reason}" for f, reason in bypassed_files])
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed: {details}")

def test_clean_corpus_preserved():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Directory {CLEAN_CORPUS_DIR} does not exist."
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    assert len(clean_files) > 0, f"No CSV files found in {CLEAN_CORPUS_DIR}."

    modified_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)

        with open(filepath, 'r') as f:
            expected_content = f.read().strip()

        returncode, stdout, stderr = run_filter_script(filepath)

        if returncode != 0:
            modified_files.append((filename, f"Script exited with code {returncode}"))
            continue

        actual_content = stdout.strip()
        if actual_content != expected_content:
            modified_files.append((filename, "Output did not match input exactly"))

    if modified_files:
        details = ", ".join([f"{f}: {reason}" for f, reason in modified_files])
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean files modified: {details}")