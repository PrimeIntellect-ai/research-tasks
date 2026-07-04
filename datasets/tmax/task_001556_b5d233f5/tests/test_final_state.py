# test_final_state.py

import os
import glob
import subprocess
import json
import urllib.request
import pytest

def test_services_up_and_configured():
    """Test that the Flask service is running and serving the correct threshold."""
    try:
        response = urllib.request.urlopen("http://127.0.0.1:5000/threshold", timeout=5)
        data = response.read().decode('utf-8')
        # The exact format might vary depending on how Flask serves it, but it should contain 0.85
        assert "0.85" in data, f"Expected threshold 0.85 in response, got: {data}"
    except Exception as e:
        pytest.fail(f"Failed to fetch threshold from Flask service: {e}")

def test_executable_exists():
    """Test that the C++ executable exists and is executable."""
    exe_path = "/home/user/csv_filter"
    assert os.path.isfile(exe_path), f"Executable not found at {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File at {exe_path} is not executable"

def test_adversarial_corpus():
    """Test the executable against the evil and clean corpora."""
    exe_path = "/home/user/csv_filter"

    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert len(evil_files) > 0, f"No CSV files found in {evil_dir}"
    assert len(clean_files) > 0, f"No CSV files found in {clean_dir}"

    evil_bypassed = []
    clean_modified = []

    for file_path in evil_files:
        result = subprocess.run([exe_path, file_path], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(file_path))

    for file_path in clean_files:
        result = subprocess.run([exe_path, file_path], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(file_path))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_experiment_log_exists():
    """Test that the experiment log was created."""
    log_path = "/home/user/experiment_log.txt"
    assert os.path.isfile(log_path), f"Experiment log not found at {log_path}"