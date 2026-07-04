# test_final_state.py
import os
import subprocess
import pytest

def test_incident_frame():
    filepath = "/home/user/incident_frame.txt"
    assert os.path.isfile(filepath), f"Missing file: {filepath}"
    with open(filepath, 'r') as f:
        content = f.read().strip()
    assert content == "14", f"Expected frame '14', got '{content}'"

def test_manifest_filter_executable():
    executable = "/home/user/filter_manifest"
    assert os.path.isfile(executable), f"Missing executable at {executable}"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable"

def test_manifest_filter_clean_corpus():
    executable = "/home/user/filter_manifest"
    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"Missing clean directory: {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No clean corpus files found to test."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([executable, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (expected exit code 0, got otherwise): {', '.join(failed_files)}")

def test_manifest_filter_evil_corpus():
    executable = "/home/user/filter_manifest"
    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"Missing evil directory: {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No evil corpus files found to test."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([executable, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (expected exit code 1, got otherwise): {', '.join(failed_files)}")