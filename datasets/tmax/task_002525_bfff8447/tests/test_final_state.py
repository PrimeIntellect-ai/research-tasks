# test_final_state.py
import os
import csv
from collections import defaultdict

def test_output_file_exists():
    output_path = "/home/user/output/merged_sensors.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

def test_output_content_correct():
    output_path = "/home/user/output/merged_sensors.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    # Read inputs and compute expected output
    sensor_files = {
        'A': "/home/user/data/sensor_A.csv",
        'B': "/home/user/data/sensor_B.csv",
        'C': "/home/user/data/sensor_C.csv"
    }

    buckets = defaultdict(lambda: {'A': [], 'B': [], 'C': []})

    for sensor, filepath in sensor_files.items():
        if not os.path.isfile(filepath):
            continue
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) != 2:
                    continue
                try:
                    ts = int(parts[0])
                    val = float(parts[1])
                    bucket_ts = (ts // 60) * 60
                    buckets[bucket_ts][sensor].append(val)
                except ValueError:
                    continue

    expected_rows = []
    for bucket_ts in sorted(buckets.keys()):
        row = [str(bucket_ts)]
        for sensor in ['A', 'B', 'C']:
            vals = buckets[bucket_ts][sensor]
            if vals:
                avg = sum(vals) / len(vals)
                row.append(f"{avg:.2f}")
            else:
                row.append("-999.00")
        expected_rows.append(",".join(row))

    expected_header = "bucket_timestamp,avg_A,avg_B,avg_C"

    # Read actual output
    with open(output_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) > 0, "Output file is empty."
    assert actual_lines[0] == expected_header, f"Header is incorrect. Expected: {expected_header}, Got: {actual_lines[0]}"

    actual_data = actual_lines[1:]
    assert len(actual_data) == len(expected_rows), f"Expected {len(expected_rows)} data rows, but got {len(actual_data)}."

    for i, (expected, actual) in enumerate(zip(expected_rows, actual_data)):
        assert actual == expected, f"Row {i+1} mismatch. Expected: {expected}, Got: {actual}"