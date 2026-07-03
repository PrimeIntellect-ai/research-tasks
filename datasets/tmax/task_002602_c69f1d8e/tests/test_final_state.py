# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    executable_path = '/home/user/detector'
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_clean_corpus():
    """Verify that all clean files are accepted (exit code 0)."""
    executable_path = '/home/user/detector'
    clean_dir = '/app/clean'
    clean_files = glob.glob(os.path.join(clean_dir, '*.csv'))

    assert len(clean_files) > 0, f"No clean files found in {clean_dir}."

    failed_files = []
    for f in clean_files:
        result = subprocess.run([executable_path, f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}"

def test_evil_corpus():
    """Verify that all evil files are rejected (exit code 1)."""
    executable_path = '/home/user/detector'
    evil_dir = '/app/evil'
    evil_files = glob.glob(os.path.join(evil_dir, '*.csv'))

    assert len(evil_files) > 0, f"No evil files found in {evil_dir}."

    failed_files = []
    for f in evil_files:
        result = subprocess.run([executable_path, f], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}"