# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_log_detector_executable_exists():
    """Ensure the log_detector executable exists and is executable."""
    executable_path = "/home/user/log_detector"
    assert os.path.isfile(executable_path), f"Executable not found: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File is not executable: {executable_path}"

def test_clean_corpus():
    """Ensure all clean corpus files return exit code 0."""
    executable_path = "/home/user/log_detector"
    clean_dir = "/app/verifier/corpus/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert len(clean_files) > 0, f"No clean files found in {clean_dir}"

    failed_files = []
    for file_path in clean_files:
        result = subprocess.run([executable_path, file_path], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    """Ensure all evil corpus files return exit code 1."""
    executable_path = "/home/user/log_detector"
    evil_dir = "/app/verifier/corpus/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(evil_files) > 0, f"No evil files found in {evil_dir}"

    failed_files = []
    for file_path in evil_files:
        result = subprocess.run([executable_path, file_path], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed/accepted. Offending files: {', '.join(failed_files)}")