# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_sanitize_script_exists():
    assert os.path.isfile("/home/user/sanitize.sh"), "The sanitize.sh script was not found at /home/user/sanitize.sh"

def test_reference_solution_exists():
    assert os.path.isfile("/tmp/reference_solution.csv"), "The reference solution was not generated at /tmp/reference_solution.csv"

def test_adversarial_corpus_filtering():
    script_path = "/home/user/sanitize.sh"
    clean_corpus = "/app/corpus/clean"
    evil_corpus = "/app/corpus/evil"

    assert os.path.isdir(clean_corpus), "Clean corpus missing"
    assert os.path.isdir(evil_corpus), "Evil corpus missing"

    clean_files = set(f for f in os.listdir(clean_corpus) if f.endswith(".csv"))
    evil_files = set(f for f in os.listdir(evil_corpus) if f.endswith(".csv"))

    with tempfile.TemporaryDirectory() as clean_out_dir, tempfile.TemporaryDirectory() as evil_out_dir:
        # Run on clean corpus
        result_clean = subprocess.run(
            ["bash", script_path, clean_corpus, clean_out_dir],
            capture_output=True, text=True
        )
        assert result_clean.returncode == 0, f"Script failed on clean corpus:\n{result_clean.stderr}"

        # Run on evil corpus
        result_evil = subprocess.run(
            ["bash", script_path, evil_corpus, evil_out_dir],
            capture_output=True, text=True
        )
        assert result_evil.returncode == 0, f"Script failed on evil corpus:\n{result_evil.stderr}"

        # Check clean output
        clean_out_files = set(f for f in os.listdir(clean_out_dir) if f.endswith(".csv"))
        missing_clean = clean_files - clean_out_files

        # Check evil output
        evil_out_files = set(f for f in os.listdir(evil_out_dir) if f.endswith(".csv"))
        bypassed_evil = evil_out_files

        error_msgs = []
        if missing_clean:
            error_msgs.append(f"{len(missing_clean)} of {len(clean_files)} clean modified/rejected. Examples: {list(missing_clean)[:3]}")
        if bypassed_evil:
            error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed. Examples: {list(bypassed_evil)[:3]}")

        if error_msgs:
            pytest.fail(" | ".join(error_msgs))