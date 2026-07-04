# test_final_state.py
import os
import subprocess
import pytest
import glob

def test_artifact_filter_exists():
    binary_path = "/home/user/artifact_filter"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

def test_artifact_filter_clean_corpus():
    binary_path = "/home/user/artifact_filter"
    if not os.path.exists(binary_path):
        pytest.fail("Binary /home/user/artifact_filter does not exist.")

    clean_dir = "/app/corpora/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*"))

    assert len(clean_files) > 0, "No files found in clean corpus"

    failed_files = []
    for filepath in clean_files:
        if not os.path.isfile(filepath):
            continue
        result = subprocess.run([binary_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}")

def test_artifact_filter_evil_corpus():
    binary_path = "/home/user/artifact_filter"
    if not os.path.exists(binary_path):
        pytest.fail("Binary /home/user/artifact_filter does not exist.")

    evil_dir = "/app/corpora/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(evil_files) > 0, "No files found in evil corpus"

    failed_files = []
    for filepath in evil_files:
        if not os.path.isfile(filepath):
            continue
        result = subprocess.run([binary_path, filepath], capture_output=True)
        if result.returncode == 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}")