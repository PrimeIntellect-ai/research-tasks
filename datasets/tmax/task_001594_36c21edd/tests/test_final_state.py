# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/filter_sims"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"The path {SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"The script {SCRIPT_PATH} is not executable."

def test_clean_corpus_preserved():
    # Run the script on the clean corpus
    result = subprocess.run([SCRIPT_PATH, CLEAN_CORPUS_DIR], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed on clean corpus with return code {result.returncode}. Stderr: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    output_basenames = set(os.path.basename(path) for path in output_lines)

    expected_files = set(f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f)))

    missing_clean = expected_files - output_basenames
    extra_clean = output_basenames - expected_files

    error_msg = []
    if missing_clean:
        error_msg.append(f"{len(missing_clean)} of {len(expected_files)} clean files modified/rejected: {', '.join(sorted(missing_clean))}")
    if extra_clean:
        error_msg.append(f"Unexpected files preserved in clean corpus output: {', '.join(sorted(extra_clean))}")

    assert not error_msg, "; ".join(error_msg)

def test_evil_corpus_rejected():
    # Run the script on the evil corpus
    result = subprocess.run([SCRIPT_PATH, EVIL_CORPUS_DIR], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed on evil corpus with return code {result.returncode}. Stderr: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    output_basenames = set(os.path.basename(path) for path in output_lines)

    evil_files = set(f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f)))

    bypassed_evil = output_basenames.intersection(evil_files)

    if bypassed_evil:
        pytest.fail(f"{len(bypassed_evil)} of {len(evil_files)} evil files bypassed: {', '.join(sorted(bypassed_evil))}")