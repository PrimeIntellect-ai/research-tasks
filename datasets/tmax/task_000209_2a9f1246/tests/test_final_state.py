# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_artifact_filter_exists_and_executable():
    binary_path = "/home/user/artifact_filter"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable."

def test_corpora_filtering():
    binary_path = "/home/user/artifact_filter"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_files) > 0, "No clean CSV files found in /app/corpora/clean."
    assert len(evil_files) > 0, "No evil CSV files found in /app/corpora/evil."

    clean_failed = []
    for f in clean_files:
        result = subprocess.run([binary_path, f], capture_output=True, text=True)
        # Clean files should exit with 0 and print STATUS: CLEAN
        if result.returncode != 0 or "STATUS: CLEAN" not in result.stdout:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        result = subprocess.run([binary_path, f], capture_output=True, text=True)
        # Evil files should exit with 1 and print STATUS: LEAKED
        if result.returncode != 1 or "STATUS: LEAKED" not in result.stdout:
            evil_failed.append(os.path.basename(f))

    errors = []
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))