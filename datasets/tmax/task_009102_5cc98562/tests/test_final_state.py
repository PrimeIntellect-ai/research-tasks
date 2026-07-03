# test_final_state.py

import os
import json
import re
import pytest

def test_transformed_artifacts_json():
    """Verify the transformed_artifacts.json file exists and has the correct structure."""
    file_path = '/home/user/transformed_artifacts.json'
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    assert isinstance(data, list), "JSON data should be an array."
    assert len(data) == 10000, f"Expected 10000 entries, found {len(data)}."

    # Check first entry
    first_entry = data[0]
    assert first_entry.get('id') == 1, f"Expected first entry id to be 1, got {first_entry.get('id')}."
    assert first_entry.get('filename') == 'build_bin_1.zip', f"Expected first entry filename to be 'build_bin_1.zip', got '{first_entry.get('filename')}'."
    assert isinstance(first_entry.get('total_coverage'), (int, float)), "total_coverage should be a number."

    # Check last entry
    last_entry = data[-1]
    assert last_entry.get('id') == 10000, f"Expected last entry id to be 10000, got {last_entry.get('id')}."
    assert last_entry.get('filename') == 'build_bin_10000.zip', f"Expected last entry filename to be 'build_bin_10000.zip', got '{last_entry.get('filename')}'."
    assert isinstance(last_entry.get('total_coverage'), (int, float)), "total_coverage should be a number."

def test_benchmark_log():
    """Verify the benchmark.log file exists and matches the required format."""
    file_path = '/home/user/benchmark.log'
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        log_content = f.read().strip()

    pattern = re.compile(r"^Processed 10000 messages in \d+\.\d{4} seconds\. Throughput: \d+\.\d{4} msgs/sec\.$")
    assert pattern.match(log_content), f"Benchmark log format is incorrect. Got: '{log_content}'"

def test_scripts_exist():
    """Verify that the required scripts were created."""
    scripts = [
        "/home/user/ws_server.py",
        "/home/user/ws_client.py",
        "/home/user/run.sh"
    ]
    for script in scripts:
        assert os.path.exists(script), f"Required script {script} does not exist."