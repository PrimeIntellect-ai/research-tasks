# test_final_state.py

import os
import csv
import pytest

def test_local_configs_copied():
    remote_dir = "/home/user/remote_configs"
    local_dir = "/home/user/local_configs"

    assert os.path.isdir(local_dir), f"Directory {local_dir} is missing."

    remote_files = set(f for f in os.listdir(remote_dir) if f.endswith('.json'))
    local_files = set(f for f in os.listdir(local_dir) if f.endswith('.json'))

    missing_files = remote_files - local_files
    assert not missing_files, f"Files missing in local_configs: {missing_files}"

def test_invalid_files_txt():
    invalid_files_path = "/home/user/invalid_files.txt"
    assert os.path.isfile(invalid_files_path), f"File {invalid_files_path} is missing."

    expected_invalid_files = [
        "/home/user/local_configs/srv2_t2.json",
        "/home/user/local_configs/srv3_t1.json"
    ]

    with open(invalid_files_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_invalid_files, (
        f"Contents of {invalid_files_path} do not match expected.\n"
        f"Expected: {expected_invalid_files}\n"
        f"Found: {lines}"
    )

def test_anomalies_csv():
    anomalies_path = "/home/user/anomalies.csv"
    assert os.path.isfile(anomalies_path), f"File {anomalies_path} is missing."

    expected_header = ["server_id", "metric_name", "old_value", "new_value", "timestamp"]
    expected_rows = [
        ["srv1", "max_conn", "100.0", "160.0", "2"],
        ["srv2", "max_conn", "500.0", "200.0", "3"]
    ]

    with open(anomalies_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"File {anomalies_path} is empty."

    header = rows[0]
    assert header == expected_header, (
        f"CSV header does not match expected.\n"
        f"Expected: {expected_header}\n"
        f"Found: {header}"
    )

    data_rows = rows[1:]
    assert data_rows == expected_rows, (
        f"CSV data rows do not match expected.\n"
        f"Expected: {expected_rows}\n"
        f"Found: {data_rows}"
    )