# test_final_state.py

import os
import json
import subprocess
import pytest

def test_root_cause_json_exists_and_valid():
    """Test that root_cause.json exists and is valid JSON."""
    file_path = "/home/user/root_cause.json"
    assert os.path.exists(file_path), f"Expected file {file_path} is missing."
    assert os.path.isfile(file_path), f"Expected {file_path} to be a file."

    try:
        with open(file_path, 'r') as f:
            json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"File {file_path} is not valid JSON: {e}")

def test_root_cause_json_content():
    """Test that root_cause.json contains the correct findings."""
    file_path = "/home/user/root_cause.json"
    assert os.path.exists(file_path), f"Expected file {file_path} is missing."

    with open(file_path, 'r') as f:
        data = json.load(f)

    assert "crash_timestamp" in data, "Key 'crash_timestamp' is missing from root_cause.json."
    assert "crashing_seq_id" in data, "Key 'crashing_seq_id' is missing from root_cause.json."
    assert "buggy_function" in data, "Key 'buggy_function' is missing from root_cause.json."

    assert data["crash_timestamp"] == "2024-05-10 14:32:08", f"Expected crash_timestamp to be '2024-05-10 14:32:08', got {data['crash_timestamp']}."
    assert data["crashing_seq_id"] == 102, f"Expected crashing_seq_id to be 102, got {data['crashing_seq_id']}."
    assert data["buggy_function"] == "process_metrics", f"Expected buggy_function to be 'process_metrics', got {data['buggy_function']}."

def test_fixed_cpp_exists_and_compiles():
    """Test that metrics_processor_fixed.cpp exists and compiles successfully."""
    file_path = "/home/user/metrics_processor_fixed.cpp"
    assert os.path.exists(file_path), f"Expected file {file_path} is missing."
    assert os.path.isfile(file_path), f"Expected {file_path} to be a file."

    compile_cmd = ["g++", "-std=c++17", "-o", "/tmp/fixed_test", file_path]

    try:
        result = subprocess.run(compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Compilation of {file_path} failed.\nCommand: {' '.join(compile_cmd)}\nError output:\n{e.stderr}")

    assert os.path.exists("/tmp/fixed_test"), "Compiled executable /tmp/fixed_test was not created."