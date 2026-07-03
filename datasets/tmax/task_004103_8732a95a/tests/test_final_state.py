# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_validate_dataset_binary_exists():
    bin_path = "/home/user/validate_dataset"
    assert os.path.exists(bin_path), f"Binary missing at {bin_path}. Did you compile your C program?"
    assert os.path.isfile(bin_path), f"{bin_path} is not a file."
    assert os.access(bin_path, os.X_OK), f"{bin_path} is not executable."

def test_adversarial_corpus():
    bin_path = "/home/user/validate_dataset"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = sorted(glob.glob(os.path.join(clean_dir, "*.csv")))
    evil_files = sorted(glob.glob(os.path.join(evil_dir, "*.csv")))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}."
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}."

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run([bin_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run([bin_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    assert not error_messages, " | ".join(error_messages)