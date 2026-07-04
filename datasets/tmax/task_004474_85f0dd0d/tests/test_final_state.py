# test_final_state.py

import os
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/trace_filter.py"
CLEAN_CORPUS = "/app/corpora/clean"
EVIL_CORPUS = "/app/corpora/evil"

def test_trace_filter_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Agent script missing: {SCRIPT_PATH}"

def test_clean_corpus_accepted():
    assert os.path.isfile(SCRIPT_PATH), f"Agent script missing: {SCRIPT_PATH}"

    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = ["python3", SCRIPT_PATH, "--input", CLEAN_CORPUS, "--output", tmpdir]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed on clean corpus:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

        accepted_dir = os.path.join(tmpdir, "accepted")
        rejected_dir = os.path.join(tmpdir, "rejected")

        accepted_files = set(os.listdir(accepted_dir)) if os.path.isdir(accepted_dir) else set()
        rejected_files = set(os.listdir(rejected_dir)) if os.path.isdir(rejected_dir) else set()

        clean_input_files = set(f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.csv'))

        missing_accepted = clean_input_files - accepted_files
        false_rejected = rejected_files.intersection(clean_input_files)

        assert not false_rejected, f"{len(false_rejected)} of {len(clean_input_files)} clean files were incorrectly rejected. Examples: {list(false_rejected)[:5]}"
        assert not missing_accepted, f"{len(missing_accepted)} clean files were missing from accepted directory. Examples: {list(missing_accepted)[:5]}"

def test_evil_corpus_rejected():
    assert os.path.isfile(SCRIPT_PATH), f"Agent script missing: {SCRIPT_PATH}"

    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = ["python3", SCRIPT_PATH, "--input", EVIL_CORPUS, "--output", tmpdir]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed on evil corpus:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

        accepted_dir = os.path.join(tmpdir, "accepted")
        rejected_dir = os.path.join(tmpdir, "rejected")

        accepted_files = set(os.listdir(accepted_dir)) if os.path.isdir(accepted_dir) else set()
        rejected_files = set(os.listdir(rejected_dir)) if os.path.isdir(rejected_dir) else set()

        evil_input_files = set(f for f in os.listdir(EVIL_CORPUS) if f.endswith('.csv'))

        missing_rejected = evil_input_files - rejected_files
        false_accepted = accepted_files.intersection(evil_input_files)

        assert not false_accepted, f"{len(false_accepted)} of {len(evil_input_files)} evil files bypassed the filter (incorrectly accepted). Examples: {list(false_accepted)[:5]}"
        assert not missing_rejected, f"{len(missing_rejected)} evil files were missing from rejected directory. Examples: {list(missing_rejected)[:5]}"