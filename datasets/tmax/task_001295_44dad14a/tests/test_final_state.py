# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_executable_exists():
    """Verify that the compiled loc_check executable exists and is executable."""
    executable_path = "/home/user/loc_check"
    assert os.path.exists(executable_path), f"Executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"

def test_clean_corpus():
    """Verify that all clean corpus files are accepted (exit code 0)."""
    executable_path = "/home/user/loc_check"
    clean_dir = "/app/corpus/clean/"
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert len(clean_files) > 0, f"No clean CSV files found in {clean_dir}"

    failed_files = []
    for file_path in clean_files:
        result = subprocess.run([executable_path, file_path], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (exit code != 0): {', '.join(failed_files)}")

def test_evil_corpus():
    """Verify that all evil corpus files are rejected (exit code != 0)."""
    executable_path = "/home/user/loc_check"
    evil_dir = "/app/corpus/evil/"
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(evil_files) > 0, f"No evil CSV files found in {evil_dir}"

    bypassed_files = []
    for file_path in evil_files:
        result = subprocess.run([executable_path, file_path], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(file_path))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed the filter (exit code == 0): {', '.join(bypassed_files)}")