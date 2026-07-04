# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_filter_executable_exists():
    filter_path = "/home/user/filter"
    assert os.path.isfile(filter_path), f"Executable {filter_path} does not exist."
    assert os.access(filter_path, os.X_OK), f"Executable {filter_path} is not executable."

def test_adversarial_corpus():
    filter_path = "/home/user/filter"
    clean_dir = "/home/user/data/clean"
    evil_dir = "/home/user/data/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run([filter_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run([filter_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))