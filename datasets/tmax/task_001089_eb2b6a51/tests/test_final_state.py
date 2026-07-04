# test_final_state.py
import os
import shutil
import subprocess
import tempfile
import pytest

def test_recovered_config():
    config_path = "/home/user/recovered_config.txt"
    assert os.path.isfile(config_path), f"Missing recovered config file: {config_path}"

    with open(config_path, "r") as f:
        content = f.read().strip()

    assert content == "0.00001", f"Expected recovered config to be '0.00001', got '{content}'"

def test_log_filter_script_exists():
    script_path = "/home/user/log_filter.py"
    assert os.path.isfile(script_path), f"Missing log filter script: {script_path}"

def test_log_filter_clean_corpus():
    script_path = "/home/user/log_filter.py"
    clean_corpus_dir = "/app/corpus/clean"

    if not os.path.isdir(clean_corpus_dir):
        pytest.skip(f"Clean corpus dir missing: {clean_corpus_dir}")

    clean_files = [f for f in os.listdir(clean_corpus_dir) if f.endswith('.json')]
    if not clean_files:
        pytest.skip("No json files found in clean corpus.")

    with tempfile.TemporaryDirectory() as valid_dir, tempfile.TemporaryDirectory() as invalid_dir:
        result = subprocess.run(
            ["python3", script_path, clean_corpus_dir, valid_dir, invalid_dir],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"log_filter.py failed on clean corpus. Stderr: {result.stderr}"

        valid_output_files = set(os.listdir(valid_dir))
        invalid_output_files = set(os.listdir(invalid_dir))

        failed_clean = set(clean_files) - valid_output_files
        assert not failed_clean, f"{len(failed_clean)} of {len(clean_files)} clean files modified/rejected. Missing from valid dir: {list(failed_clean)[:5]}"
        assert not invalid_output_files, f"Clean files incorrectly placed in invalid dir: {list(invalid_output_files)[:5]}"

def test_log_filter_evil_corpus():
    script_path = "/home/user/log_filter.py"
    evil_corpus_dir = "/app/corpus/evil"

    if not os.path.isdir(evil_corpus_dir):
        pytest.skip(f"Evil corpus dir missing: {evil_corpus_dir}")

    evil_files = [f for f in os.listdir(evil_corpus_dir) if f.endswith('.json')]
    if not evil_files:
        pytest.skip("No json files found in evil corpus.")

    with tempfile.TemporaryDirectory() as valid_dir, tempfile.TemporaryDirectory() as invalid_dir:
        result = subprocess.run(
            ["python3", script_path, evil_corpus_dir, valid_dir, invalid_dir],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"log_filter.py failed on evil corpus. Stderr: {result.stderr}"

        valid_output_files = set(os.listdir(valid_dir))
        invalid_output_files = set(os.listdir(invalid_dir))

        failed_evil = set(evil_files) - invalid_output_files
        assert not failed_evil, f"{len(failed_evil)} of {len(evil_files)} evil files bypassed. Missing from invalid dir: {list(failed_evil)[:5]}"
        assert not valid_output_files, f"Evil files incorrectly placed in valid dir: {list(valid_output_files)[:5]}"