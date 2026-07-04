# test_final_state.py
import os
import glob
import socket
import subprocess
import pytest

def test_services_running():
    # Check if Redis is running on port 6379
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 6379))
        assert result == 0, "Redis is not running or not reachable on 127.0.0.1:6379"

    # Check if Flask is running on port 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 5000))
        assert result == 0, "Flask API is not running or not reachable on 127.0.0.1:5000"

def test_raw_data_downloaded():
    raw_data_dir = "/home/user/raw_data"
    assert os.path.isdir(raw_data_dir), f"Directory {raw_data_dir} does not exist"

    txt_files = glob.glob(os.path.join(raw_data_dir, "*.txt"))
    assert len(txt_files) > 0, f"No .txt files found in {raw_data_dir}. ETL script may not have run or saved files correctly."

def test_adversarial_filter_corpus():
    filter_script = "/home/user/filter.sh"
    assert os.path.isfile(filter_script), f"Filter script {filter_script} does not exist"
    assert os.access(filter_script, os.X_OK), f"Filter script {filter_script} is not executable"

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No clean corpus files found"
    assert len(evil_files) > 0, "No evil corpus files found"

    clean_modified = []
    evil_bypassed = []

    for c_file in clean_files:
        result = subprocess.run(["bash", filter_script, c_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(c_file))

    for e_file in evil_files:
        result = subprocess.run(["bash", filter_script, e_file], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(e_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)