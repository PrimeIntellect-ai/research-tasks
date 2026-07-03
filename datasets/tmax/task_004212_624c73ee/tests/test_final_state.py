# test_final_state.py
import os
import subprocess
import pytest

def test_fast_checker_exists_and_executable():
    path = "/home/user/fast_checker"
    assert os.path.exists(path), f"Missing compiled binary: {path}"
    assert os.path.isfile(path), f"{path} is not a file"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_clean_corpus_accepted():
    binary_path = "/home/user/fast_checker"
    corpus_dir = "/app/corpora/clean"

    assert os.path.isdir(corpus_dir), f"Missing clean corpus directory: {corpus_dir}"

    failed_files = []
    total_files = 0

    for filename in os.listdir(corpus_dir):
        filepath = os.path.join(corpus_dir, filename)
        if os.path.isfile(filepath):
            total_files += 1
            result = subprocess.run([binary_path, filepath], capture_output=True)
            if result.returncode != 0:
                failed_files.append(filename)

    assert total_files > 0, "No files found in clean corpus"
    assert len(failed_files) == 0, f"{len(failed_files)} of {total_files} clean files were rejected (expected exit 0). Offending files: {', '.join(failed_files[:10])}"

def test_evil_corpus_rejected():
    binary_path = "/home/user/fast_checker"
    corpus_dir = "/app/corpora/evil"

    assert os.path.isdir(corpus_dir), f"Missing evil corpus directory: {corpus_dir}"

    failed_files = []
    total_files = 0

    for filename in os.listdir(corpus_dir):
        filepath = os.path.join(corpus_dir, filename)
        if os.path.isfile(filepath):
            total_files += 1
            result = subprocess.run([binary_path, filepath], capture_output=True)
            if result.returncode == 0:
                failed_files.append(filename)

    assert total_files > 0, "No files found in evil corpus"
    assert len(failed_files) == 0, f"{len(failed_files)} of {total_files} evil files bypassed the checker (expected non-zero exit). Offending files: {', '.join(failed_files[:10])}"