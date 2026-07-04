# test_final_state.py

import os
import subprocess
import pytest

def test_auth_filter_exists_and_executable():
    binary_path = "/home/user/auth_filter"
    assert os.path.exists(binary_path), f"The binary {binary_path} does not exist. Did you compile your Go code?"
    assert os.path.isfile(binary_path), f"{binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"The binary {binary_path} is not executable."

def test_adversarial_corpus():
    binary_path = "/home/user/auth_filter"
    evil_dir = "/app/evil_tokens"
    clean_dir = "/app/clean_tokens"

    assert os.path.exists(evil_dir), f"Evil tokens directory {evil_dir} is missing."
    assert os.path.exists(clean_dir), f"Clean tokens directory {clean_dir} is missing."

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No evil tokens found to test."
    assert len(clean_files) > 0, "No clean tokens found to test."

    evil_bypassed = []
    clean_rejected = []

    # Test evil tokens (expect exit code 1)
    for evil_file in evil_files:
        result = subprocess.run([binary_path, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    # Test clean tokens (expect exit code 0)
    for clean_file in clean_files:
        result = subprocess.run([binary_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil tokens bypassed the filter: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean tokens were rejected by the filter: {', '.join(clean_rejected)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))