# test_final_state.py
import os
import csv
import json
import math
import pytest

def test_script_executable():
    """Verify that the migration script exists and is executable."""
    script_path = "/home/user/migrate.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_json_output_correctness():
    """Verify that the JSON output is correctly derived from the CSV."""
    csv_path = "/home/user/artifacts/registry.csv"
    json_path = "/home/user/artifacts/new_registry.json"

    assert os.path.isfile(csv_path), f"Original CSV file {csv_path} is missing."
    assert os.path.isfile(json_path), f"JSON output file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {json_path} is not valid JSON.")

    assert isinstance(actual_json, list), "JSON output must be an array of objects."

    expected_json = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            size_bytes = int(row['size_bytes'])
            size_mb_raw = size_bytes / 1048576.0
            # Format strictly to two decimal places as required
            size_mb = float(f"{size_mb_raw:.2f}")

            # Calculate storage_index based on the rounded size_mb
            storage_index = math.ceil(math.sqrt(size_mb) * 1.5)

            expected_json.append({
                "id": row['id'],
                "filename": row['filename'],
                "size_mb": size_mb,
                "storage_index": storage_index
            })

    assert len(actual_json) == len(expected_json), "JSON array length does not match CSV row count."

    for actual, expected in zip(actual_json, expected_json):
        assert actual.get('id') == expected['id'], f"Expected id '{expected['id']}', got '{actual.get('id')}'"
        assert actual.get('filename') == expected['filename'], f"Expected filename '{expected['filename']}', got '{actual.get('filename')}'"

        actual_size_mb = actual.get('size_mb')
        assert actual_size_mb is not None, "Missing 'size_mb' field in JSON object."
        assert math.isclose(actual_size_mb, expected['size_mb'], rel_tol=1e-5), \
            f"Expected size_mb {expected['size_mb']} for {expected['id']}, got {actual_size_mb}"

        actual_storage_index = actual.get('storage_index')
        assert actual_storage_index is not None, "Missing 'storage_index' field in JSON object."
        assert actual_storage_index == expected['storage_index'], \
            f"Expected storage_index {expected['storage_index']} for {expected['id']}, got {actual_storage_index}"

def test_benchmark_log():
    """Verify that the benchmark log exists and contains a valid user CPU time numeric value."""
    log_path = "/home/user/artifacts/benchmark.log"
    assert os.path.isfile(log_path), f"Benchmark log {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content, "Benchmark log is empty."

    try:
        cpu_time = float(content)
        assert cpu_time >= 0, "CPU time in benchmark log cannot be negative."
    except ValueError:
        pytest.fail(f"Benchmark log does not contain a valid numeric value. Found: '{content}'")