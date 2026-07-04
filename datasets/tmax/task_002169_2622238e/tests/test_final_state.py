# test_final_state.py

import os
import re
import csv
from collections import defaultdict
import pytest

def test_run_pipeline_script_exists_and_executable():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_aggregate_script_exists():
    script_path = '/home/user/aggregate.py'
    assert os.path.isfile(script_path), f"Expected Python script {script_path} does not exist."

def test_hourly_averages_csv_exists():
    csv_path = '/home/user/hourly_averages.csv'
    assert os.path.isfile(csv_path), f"Expected output file {csv_path} does not exist."

def test_hourly_averages_content():
    raw_data_dir = '/home/user/raw_data/'
    assert os.path.isdir(raw_data_dir), f"Raw data directory {raw_data_dir} is missing."

    # Regex for valid data line
    valid_line_re = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}):\d{2}:\d{2},([a-zA-Z0-9]+),temp,(\d+(?:\.\d+)?)$')

    # Recompute expected results
    sums = defaultdict(float)
    counts = defaultdict(int)

    for filename in os.listdir(raw_data_dir):
        if not filename.endswith('.csv'):
            continue
        filepath = os.path.join(raw_data_dir, filename)
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                match = valid_line_re.match(line)
                if match:
                    hour_str = match.group(1) + ":00:00"
                    sensor_id = match.group(2)
                    temp = float(match.group(3))
                    key = (hour_str, sensor_id)
                    sums[key] += temp
                    counts[key] += 1

    expected_rows = []
    for key in sums:
        avg = sums[key] / counts[key]
        expected_rows.append((key[0], key[1], f"{avg:.2f}"))

    # Sort chronologically, then by sensor_id
    expected_rows.sort(key=lambda x: (x[0], x[1]))

    # Read actual results
    csv_path = '/home/user/hourly_averages.csv'
    actual_rows = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['timestamp', 'sensor_id', 'avg_temp'], f"Incorrect header in output CSV: {header}"
        for row in reader:
            if row:
                actual_rows.append(tuple(row))

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}."