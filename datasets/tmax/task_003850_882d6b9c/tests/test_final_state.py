# test_final_state.py

import csv
import os
from datetime import datetime, timedelta

def get_bucket(ts):
    minute = (ts.minute // 5) * 5
    return ts.replace(minute=minute, second=0, microsecond=0)

def test_error_trends_file_exists():
    assert os.path.exists('/home/user/error_trends.csv'), "The file /home/user/error_trends.csv was not created."
    assert os.path.isfile('/home/user/error_trends.csv'), "/home/user/error_trends.csv is not a regular file."

def test_error_trends_content():
    input_file = '/home/user/system_logs.csv'
    output_file = '/home/user/error_trends.csv'

    assert os.path.exists(input_file), f"Input file {input_file} is missing, cannot verify."
    assert os.path.exists(output_file), f"Output file {output_file} is missing."

    # Read input and compute expected dynamically
    earliest = None
    latest = None
    counts = {}

    with open(input_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = datetime.strptime(row['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
            if earliest is None or ts < earliest:
                earliest = ts
            if latest is None or ts > latest:
                latest = ts

            if row['level'] == 'ERROR':
                b = get_bucket(ts)
                counts[b] = counts.get(b, 0) + 1

    expected_rows = []
    if earliest is not None:
        start_bucket = get_bucket(earliest)
        end_bucket = get_bucket(latest)

        current = start_bucket
        buckets = []
        while current <= end_bucket:
            buckets.append(current)
            current += timedelta(minutes=5)

        history = []
        for b in buckets:
            c = counts.get(b, 0)
            history.append(c)
            window = history[-3:]
            sma = sum(window) / len(window)

            expected_rows.append({
                'bucket_start': b.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'error_count': str(c),
                'sma_3': f"{sma:.2f}"
            })

    # Read actual output
    with open(output_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        actual_rows = list(reader)

    expected_headers = ['bucket_start', 'error_count', 'sma_3']
    assert reader.fieldnames == expected_headers, f"Headers in output file are incorrect. Expected {expected_headers}, got {reader.fieldnames}"

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, but got {len(actual_rows)}. Ensure continuous 5-minute buckets are generated."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual['bucket_start'] == expected['bucket_start'], f"Row {i+1}: expected bucket_start {expected['bucket_start']}, got {actual['bucket_start']}"
        assert actual['error_count'] == expected['error_count'], f"Row {i+1} ({expected['bucket_start']}): expected error_count {expected['error_count']}, got {actual['error_count']}"
        assert actual['sma_3'] == expected['sma_3'], f"Row {i+1} ({expected['bucket_start']}): expected sma_3 {expected['sma_3']}, got {actual['sma_3']}"