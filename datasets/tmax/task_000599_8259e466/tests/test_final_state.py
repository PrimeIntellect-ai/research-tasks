# test_final_state.py
import os
import json
import pytest

def test_fixed_script_exists():
    script_path = '/home/user/process_sensors_fixed.py'
    assert os.path.exists(script_path), f"The fixed script {script_path} does not exist."
    with open(script_path, 'r') as f:
        content = f.read()
    assert "concurrent.futures" in content, "The fixed script must still use concurrent.futures to parallelize processing."

def test_bad_files_log():
    log_path = '/home/user/bad_files.txt'
    assert os.path.exists(log_path), f"The log file {log_path} does not exist."
    with open(log_path, 'r') as f:
        bad_files = set(line.strip() for line in f if line.strip())
    expected_bad_files = {'sensor_98.json', 'sensor_99.json'}
    assert bad_files == expected_bad_files, f"Expected {log_path} to contain {expected_bad_files}, but got {bad_files}"

def test_final_aggregate():
    aggregate_path = '/home/user/final_aggregate.json'
    assert os.path.exists(aggregate_path), f"The output file {aggregate_path} does not exist."
    with open(aggregate_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {aggregate_path} is not valid JSON.")

    assert "total" in data, f"The key 'total' is missing from {aggregate_path}."

    # 50 valid files * sum([10, 20, 30]) = 50 * 60 = 3000
    expected_total = 3000
    assert data["total"] == expected_total, f"Expected 'total' to be {expected_total}, but got {data['total']}."