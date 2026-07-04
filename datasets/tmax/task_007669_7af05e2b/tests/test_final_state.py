# test_final_state.py

import os
import csv
import re
import calendar
from datetime import datetime
import pytest

def compute_expected_summary():
    sensor_logs_path = "/home/user/sensor_logs.txt"
    server_load_path = "/home/user/server_load.csv"

    # 1. Parse sensor logs
    temp_buckets = {}
    if os.path.exists(sensor_logs_path):
        with open(sensor_logs_path, 'r') as f:
            for line in f:
                # Match e.g. [12-Oct-2023 12:02:30 UTC] ... temp: 40.5C
                ts_match = re.search(r'\[(.*?)\]', line)
                temp_match = re.search(r'temp:\s*([\d\.]+)C', line)
                if ts_match and temp_match:
                    ts_str = ts_match.group(1)
                    temp_val = float(temp_match.group(1))

                    dt = datetime.strptime(ts_str, "%d-%b-%Y %H:%M:%S UTC")
                    epoch = calendar.timegm(dt.utctimetuple())
                    bucket = epoch - (epoch % 600)

                    if bucket not in temp_buckets:
                        temp_buckets[bucket] = []
                    temp_buckets[bucket].append(temp_val)

    # 2. Parse server load
    load_buckets = {}
    if os.path.exists(server_load_path):
        with open(server_load_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if not row or len(row) < 2:
                    continue
                try:
                    epoch = int(row[0])
                    load_val = float(row[1])
                    bucket = epoch - (epoch % 600)

                    if bucket not in load_buckets:
                        load_buckets[bucket] = []
                    load_buckets[bucket].append(load_val)
                except ValueError:
                    pass

    # 3. Aggregate and Inner Join
    expected_rows = []
    common_buckets = set(temp_buckets.keys()).intersection(set(load_buckets.keys()))

    for bucket in sorted(common_buckets):
        avg_temp = sum(temp_buckets[bucket]) / len(temp_buckets[bucket])
        avg_load = sum(load_buckets[bucket]) / len(load_buckets[bucket])
        expected_rows.append({
            'interval_start_epoch': str(bucket),
            'avg_temp': f"{avg_temp:.2f}",
            'avg_load': f"{avg_load:.2f}"
        })

    return expected_rows

def test_aligned_summary_exists():
    file_path = "/home/user/aligned_summary.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist. Ensure the script creates this file."

def test_aligned_summary_contents():
    file_path = "/home/user/aligned_summary.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist."

    expected_rows = compute_expected_summary()

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['interval_start_epoch', 'avg_temp', 'avg_load'], \
            f"CSV header is incorrect. Expected ['interval_start_epoch', 'avg_temp', 'avg_load'], got {header}"

        actual_rows = []
        for row in reader:
            if row:
                actual_rows.append({
                    'interval_start_epoch': row[0],
                    'avg_temp': row[1],
                    'avg_load': row[2]
                })

    assert len(actual_rows) == len(expected_rows), \
        f"Expected {len(expected_rows)} rows (excluding header), but found {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual['interval_start_epoch'] == expected['interval_start_epoch'], \
            f"Row {i+1}: Expected interval_start_epoch {expected['interval_start_epoch']}, got {actual['interval_start_epoch']}"
        assert actual['avg_temp'] == expected['avg_temp'], \
            f"Row {i+1}: Expected avg_temp {expected['avg_temp']}, got {actual['avg_temp']}"
        assert actual['avg_load'] == expected['avg_load'], \
            f"Row {i+1}: Expected avg_load {expected['avg_load']}, got {actual['avg_load']}"