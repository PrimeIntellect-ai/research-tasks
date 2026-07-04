# test_final_state.py
import os
import subprocess
import pytest

def test_cfg_filter_exists_and_executable():
    executable_path = "/home/user/cfg_filter"
    assert os.path.isfile(executable_path), f"Missing executable: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File is not executable: {executable_path}"

def test_adversarial_corpus():
    executable_path = "/home/user/cfg_filter"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    evil_failures = []

    for clean_file in clean_files:
        result = subprocess.run([executable_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(clean_file))

    for evil_file in evil_files:
        result = subprocess.run([executable_path, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(evil_file))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean files failed (expected exit code 0): {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil files bypassed (expected exit code 1): {', '.join(evil_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))