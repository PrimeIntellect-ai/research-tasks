# test_final_state.py
import os
import subprocess
import pytest

def test_detector_binary_exists():
    binary_path = "/home/user/detector"
    assert os.path.isfile(binary_path), f"The detector binary is missing at {binary_path}."
    assert os.access(binary_path, os.X_OK), f"The detector binary at {binary_path} is not executable."

def test_clean_corpus():
    binary_path = "/home/user/detector"
    clean_dir = "/app/corpora/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."

    files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(files) > 0, "No files found in clean corpus."

    failed_files = []
    for filename in files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run([binary_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append((filename, result.returncode))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(files)} clean files failed (expected exit code 0). "
        error_msg += "Offending files: " + ", ".join([f[0] for f in failed_files])
        pytest.fail(error_msg)

def test_evil_corpus():
    binary_path = "/home/user/detector"
    evil_dir = "/app/corpora/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."

    files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(files) > 0, "No files found in evil corpus."

    failed_files = []
    for filename in files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run([binary_path, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append((filename, result.returncode))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(files)} evil files bypassed (expected exit code 1). "
        error_msg += "Offending files: " + ", ".join([f[0] for f in failed_files])
        pytest.fail(error_msg)