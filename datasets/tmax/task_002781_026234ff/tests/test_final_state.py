# test_final_state.py

import os
import subprocess
import pytest

FILTER_BIN = "/home/user/filter"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_filter_binary_exists():
    assert os.path.exists(FILTER_BIN), f"Missing required executable: {FILTER_BIN}"
    assert os.path.isfile(FILTER_BIN), f"Expected {FILTER_BIN} to be a file"
    assert os.access(FILTER_BIN, os.X_OK), f"Expected {FILTER_BIN} to be executable"

def run_filter_on_file(file_path):
    try:
        with open(file_path, 'r') as f:
            result = subprocess.run(
                [FILTER_BIN],
                stdin=f,
                capture_output=True,
                text=True,
                timeout=2
            )
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_clean_corpus_accepted():
    if not os.path.exists(CLEAN_CORPUS_DIR):
        pytest.fail(f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}")

    files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    if not files:
        pytest.fail(f"No files found in clean corpus directory: {CLEAN_CORPUS_DIR}")

    failed_files = []
    for filename in files:
        file_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        output = run_filter_on_file(file_path)
        if output != "ACCEPT":
            failed_files.append((filename, output))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(files)} clean files modified/rejected.\n"
        error_msg += "Offending files:\n" + "\n".join([f" - {f} (Output: {out})" for f, out in failed_files[:10]])
        if len(failed_files) > 10:
            error_msg += f"\n...and {len(failed_files) - 10} more."
        pytest.fail(error_msg)

def test_evil_corpus_rejected():
    if not os.path.exists(EVIL_CORPUS_DIR):
        pytest.fail(f"Evil corpus directory missing: {EVIL_CORPUS_DIR}")

    files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    if not files:
        pytest.fail(f"No files found in evil corpus directory: {EVIL_CORPUS_DIR}")

    failed_files = []
    for filename in files:
        file_path = os.path.join(EVIL_CORPUS_DIR, filename)
        output = run_filter_on_file(file_path)
        if output != "REJECT":
            failed_files.append((filename, output))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(files)} evil files bypassed.\n"
        error_msg += "Offending files:\n" + "\n".join([f" - {f} (Output: {out})" for f, out in failed_files[:10]])
        if len(failed_files) > 10:
            error_msg += f"\n...and {len(failed_files) - 10} more."
        pytest.fail(error_msg)