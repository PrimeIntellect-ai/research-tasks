# test_final_state.py

import os
import subprocess
import pytest

def test_staging_key_extracted():
    """Validates that the staging key was correctly extracted from the video."""
    key_path = "/home/user/staging_key.txt"
    assert os.path.exists(key_path), f"Staging key file not found at {key_path}"

    with open(key_path, "r") as f:
        content = f.read().strip()

    expected_key = "7a4b9c2f8d1e5a6b3c9f4d7e2a1b8c5f"
    assert content == expected_key, f"Extracted key is incorrect. Expected '{expected_key}', got '{content}'"

def test_sanitizer_binary_exists_and_executable():
    """Validates that the sanitizer binary was compiled and is executable."""
    bin_path = "/home/user/sanitizer"
    assert os.path.exists(bin_path), f"Sanitizer binary not found at {bin_path}"
    assert os.access(bin_path, os.X_OK), f"Sanitizer binary at {bin_path} is not executable"

def test_sanitizer_against_corpora():
    """
    Validates the sanitizer against the adversarial corpus.
    Must accept all clean files (exit code 0) and reject all evil files (exit code 1).
    """
    bin_path = "/home/user/sanitizer"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.exists(bin_path), f"Sanitizer binary missing at {bin_path}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "No files found in clean corpus directory."
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    clean_failures = []
    for f in clean_files:
        result = subprocess.run([bin_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run([bin_path, f], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))