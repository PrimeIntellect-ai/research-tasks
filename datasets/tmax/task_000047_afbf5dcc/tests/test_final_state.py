# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/ci_filter.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"{SCRIPT_PATH} is not executable"

def test_clean_corpus_accepted():
    result = subprocess.run([SCRIPT_PATH, CLEAN_CORPUS_DIR], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    expected_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]

    missing = set(expected_files) - set(output_lines)
    extra = set(output_lines) - set(expected_files)

    assert not missing, f"{len(missing)} of {len(expected_files)} clean files were incorrectly rejected. Missing files: {', '.join(missing)}"
    assert not extra, f"Script outputted unexpected paths for clean corpus: {', '.join(extra)}"

def test_evil_corpus_rejected():
    result = subprocess.run([SCRIPT_PATH, EVIL_CORPUS_DIR], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    # All files in evil corpus should be rejected (i.e. not outputted)
    all_evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    bypassed = set(output_lines).intersection(set(all_evil_files))

    assert not bypassed, f"{len(bypassed)} of {len(all_evil_files)} evil files bypassed the filter. Bypassed files: {', '.join(bypassed)}"
    assert not output_lines, f"Script outputted unexpected paths for evil corpus: {', '.join(output_lines)}"