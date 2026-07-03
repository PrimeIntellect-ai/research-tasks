# test_final_state.py

import os
import subprocess
import pytest

def test_filter_binary_exists():
    filter_path = "/home/user/filter"
    assert os.path.exists(filter_path), f"Missing required binary: {filter_path}"
    assert os.path.isfile(filter_path), f"Not a file: {filter_path}"
    assert os.access(filter_path, os.X_OK), f"Binary is not executable: {filter_path}"

def test_adversarial_corpus():
    filter_path = "/home/user/filter"
    clean_dir = "/hidden/corpus/clean"
    evil_dir = "/hidden/corpus/evil"

    assert os.path.exists(clean_dir), f"Missing clean corpus directory: {clean_dir}"
    assert os.path.exists(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    evil_failed = []

    for cf in clean_files:
        result = subprocess.run([filter_path, cf], capture_output=True, text=True)
        if result.returncode != 0 or "SAFE" not in result.stdout:
            clean_failed.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([filter_path, ef], capture_output=True, text=True)
        if result.returncode != 1 or "REJECT" not in result.stdout:
            evil_failed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected or crashed). Offending files: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (accepted). Offending files: {', '.join(evil_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))