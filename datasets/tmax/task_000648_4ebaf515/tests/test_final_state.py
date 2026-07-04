# test_final_state.py

import os
import subprocess
import pytest

def test_wal_sanitizer_exists():
    binary_path = "/home/user/wal_sanitizer"
    assert os.path.isfile(binary_path), f"The sanitizer binary is missing at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"The file at {binary_path} is not executable"

def test_wal_sanitizer_clean_corpus():
    binary_path = "/home/user/wal_sanitizer"
    clean_dir = "/app/wal_clean/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No files found in the clean corpus directory."

    failed_files = []

    for filepath in clean_files:
        result = subprocess.run([binary_path, filepath], capture_output=True, text=True)
        if result.returncode != 0 or "VALID" not in result.stdout:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected incorrectly. Offending files: {', '.join(failed_files)}")

def test_wal_sanitizer_evil_corpus():
    binary_path = "/home/user/wal_sanitizer"
    evil_dir = "/app/wal_evil/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No files found in the evil corpus directory."

    failed_files = []

    for filepath in evil_files:
        result = subprocess.run([binary_path, filepath], capture_output=True, text=True)
        if result.returncode != 1 or "CORRUPTED" not in result.stdout:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed validation. Offending files: {', '.join(failed_files)}")