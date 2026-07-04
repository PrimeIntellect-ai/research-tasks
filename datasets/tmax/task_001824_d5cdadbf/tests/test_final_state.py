# test_final_state.py

import os
import subprocess
import pytest

CLEAN_CORPUS_DIR = '/app/corpora/clean/'
EVIL_CORPUS_DIR = '/app/corpora/evil/'
GO_SCRIPT_PATH = '/home/user/graph_validator.go'

def run_validator(csv_path):
    """Runs the student's Go script against a CSV file and returns the output."""
    if not os.path.isfile(GO_SCRIPT_PATH):
        pytest.fail(f"Go script not found at {GO_SCRIPT_PATH}")

    try:
        result = subprocess.run(
            ['go', 'run', GO_SCRIPT_PATH, csv_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1
    except Exception as e:
        return f"ERROR: {str(e)}", -1

def test_graph_validator_clean_corpus():
    """Verify that the script ACCEPTs all clean files."""
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.fail(f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    if not clean_files:
        pytest.fail("No CSV files found in clean corpus.")

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        output, retcode = run_validator(filepath)
        if output != "ACCEPT" or retcode != 0:
            failed_files.append((filename, output, retcode))

    if failed_files:
        details = ", ".join([f"{f} (out: {o}, code: {c})" for f, o, c in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected or failed: {details}")

def test_graph_validator_evil_corpus():
    """Verify that the script REJECTs all evil files."""
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.fail(f"Evil corpus directory missing: {EVIL_CORPUS_DIR}")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]
    if not evil_files:
        pytest.fail("No CSV files found in evil corpus.")

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        output, retcode = run_validator(filepath)
        if output != "REJECT" or retcode != 0:
            failed_files.append((filename, output, retcode))

    if failed_files:
        details = ", ".join([f"{f} (out: {o}, code: {c})" for f, o, c in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed or failed: {details}")