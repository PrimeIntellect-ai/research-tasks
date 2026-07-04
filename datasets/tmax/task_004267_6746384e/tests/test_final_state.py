# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_crash_frame_extracted():
    """Check that the correct frame number was extracted and written to crash_frame.txt."""
    path = "/home/user/crash_frame.txt"
    assert os.path.isfile(path), f"Missing output file at {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "42", f"Expected '42' in {path}, but found '{content}'"

def test_classifier_executable_exists():
    """Check that the classifier program exists and is executable."""
    path = "/home/user/classifier"
    assert os.path.isfile(path), f"Missing classifier program at {path}"
    assert os.access(path, os.X_OK), f"Classifier program at {path} is not executable"

def test_classifier_clean_corpus():
    """Check that the classifier correctly identifies clean logs (exit code 0)."""
    classifier_path = "/home/user/classifier"
    clean_dir = "/app/corpus/clean"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    assert len(clean_files) > 0, f"No files found in {clean_dir}"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([classifier_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected (expected exit code 0). Offending files: {', '.join(failed_files)}")

def test_classifier_evil_corpus():
    """Check that the classifier correctly identifies evil logs (exit code 1)."""
    classifier_path = "/home/user/classifier"
    evil_dir = "/app/corpus/evil"

    evil_files = glob.glob(os.path.join(evil_dir, "*"))
    assert len(evil_files) > 0, f"No files found in {evil_dir}"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([classifier_path, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (expected exit code 1). Offending files: {', '.join(failed_files)}")

def test_supervisor_script_exists():
    """Check that the supervisor bash script exists and is executable."""
    path = "/home/user/supervisor.sh"
    assert os.path.isfile(path), f"Missing supervisor script at {path}"
    assert os.access(path, os.X_OK), f"Supervisor script at {path} is not executable"