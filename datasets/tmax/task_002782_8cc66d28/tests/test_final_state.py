# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_sanitiser_binary_exists():
    binary_path = "/home/user/sanitiser"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist. Did you compile your C++ code?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_clean_corpus():
    binary_path = "/home/user/sanitiser"
    clean_dir = "/app/corpora/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert len(clean_files) > 0, f"No clean CSV files found in {clean_dir}."

    failed_files = []
    for csv_file in clean_files:
        result = subprocess.run([binary_path, csv_file], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(csv_file))

    assert not failed_files, f"{len(failed_files)} out of {len(clean_files)} clean files were incorrectly rejected (expected exit code 0). Offending files: {failed_files[:5]}..."

def test_evil_corpus():
    binary_path = "/home/user/sanitiser"
    evil_dir = "/app/corpora/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(evil_files) > 0, f"No evil CSV files found in {evil_dir}."

    failed_files = []
    for csv_file in evil_files:
        result = subprocess.run([binary_path, csv_file], capture_output=True)
        if result.returncode != 1:
            failed_files.append((os.path.basename(csv_file), result.returncode))

    assert not failed_files, f"{len(failed_files)} out of {len(evil_files)} evil files bypassed the sanitiser (expected exit code 1). Offending files and exit codes: {failed_files[:5]}..."