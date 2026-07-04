# test_final_state.py

import os
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/filter_records.py"
CLEAN_CORPUS = "/app/clean_corpus"
EVIL_CORPUS = "/app/evil_corpus"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Agent's script not found at {SCRIPT_PATH}"

def test_filter_clean_corpus():
    with tempfile.TemporaryDirectory() as out_dir:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, "--input-dir", CLEAN_CORPUS, "--output-dir", out_dir],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Script failed on clean corpus. stderr: {result.stderr}"

        expected_files = set(os.listdir(CLEAN_CORPUS))
        actual_files = set(os.listdir(out_dir))

        missing = expected_files - actual_files
        assert not missing, f"{len(missing)} of {len(expected_files)} clean files rejected (should be accepted). Missing: {missing}"

def test_filter_evil_corpus():
    with tempfile.TemporaryDirectory() as out_dir:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, "--input-dir", EVIL_CORPUS, "--output-dir", out_dir],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Script failed on evil corpus. stderr: {result.stderr}"

        actual_files = set(os.listdir(out_dir))
        expected_files = set(os.listdir(EVIL_CORPUS))

        assert not actual_files, f"{len(actual_files)} of {len(expected_files)} evil files bypassed (should be rejected). Bypassed: {actual_files}"