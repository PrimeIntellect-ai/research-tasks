# test_final_state.py

import os
import subprocess
import pytest

def test_master_pin_file():
    path = "/home/user/master_pin.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "84920155", f"Incorrect Master PIN in {path}. Expected '84920155', got '{content}'"

def test_salt_file():
    path = "/home/user/salt.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "x9K2mP4vL8sQ1wE7", f"Incorrect salt in {path}. Expected 'x9K2mP4vL8sQ1wE7', got '{content}'"

def test_validator_executable_exists():
    path = "/home/user/validator"
    assert os.path.isfile(path), f"Missing compiled validator executable: {path}"
    assert os.access(path, os.X_OK), f"Validator executable {path} is not marked as executable"

def test_validator_clean_corpus():
    validator_path = "/home/user/validator"
    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, f"No files found in clean corpus directory: {clean_dir}"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([validator_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean tokens rejected (expected exit 0). Offending files: {', '.join(failed_files)}")

def test_validator_evil_corpus():
    validator_path = "/home/user/validator"
    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, f"No files found in evil corpus directory: {evil_dir}"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([validator_path, filepath], capture_output=True)
        if result.returncode == 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil tokens bypassed (expected exit 1). Offending files: {', '.join(failed_files)}")