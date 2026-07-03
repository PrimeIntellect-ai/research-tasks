# test_final_state.py

import os
import csv
import gzip
import json
import pytest

def get_expected_fatal_events():
    archives_dir = '/home/user/archives'
    fatal_events = []

    if not os.path.isdir(archives_dir):
        return fatal_events

    for root, _, files in os.walk(archives_dir):
        for file in files:
            if file.endswith('.json.gz'):
                file_path = os.path.join(root, file)
                try:
                    with gzip.open(file_path, 'rt') as f:
                        for line in f:
                            if not line.strip():
                                continue
                            record = json.loads(line)
                            if record.get('level') == 'FATAL':
                                stack_trace = record.get('stack_trace', '')
                                if not stack_trace:
                                    trace_lines = 0
                                else:
                                    trace_lines = len(stack_trace.split('\n'))

                                fatal_events.append({
                                    'timestamp': record.get('timestamp', ''),
                                    'service': record.get('service', ''),
                                    'trace_lines': trace_lines
                                })
                except Exception:
                    pass

    # Sort chronologically by timestamp in ascending order
    fatal_events.sort(key=lambda x: x['timestamp'])
    return fatal_events

def test_csv_exists():
    csv_path = '/home/user/fatal_summary.csv'
    assert os.path.isfile(csv_path), f"Expected output file {csv_path} does not exist."

def test_csv_contents():
    csv_path = '/home/user/fatal_summary.csv'
    assert os.path.isfile(csv_path), f"Cannot check contents, {csv_path} is missing."

    expected_events = get_expected_fatal_events()

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail("CSV file is empty, missing headers.")

        assert headers == ['timestamp', 'service', 'trace_lines'], \
            f"CSV headers are incorrect. Expected ['timestamp', 'service', 'trace_lines'], got {headers}"

        rows = list(reader)

        assert len(rows) == len(expected_events), \
            f"Expected {len(expected_events)} data rows in CSV, but found {len(rows)}."

        for i, (row, expected) in enumerate(zip(rows, expected_events)):
            assert len(row) == 3, f"Row {i+1} does not have exactly 3 columns: {row}"
            assert row[0] == expected['timestamp'], \
                f"Row {i+1} timestamp mismatch. Expected {expected['timestamp']}, got {row[0]}"
            assert row[1] == expected['service'], \
                f"Row {i+1} service mismatch. Expected {expected['service']}, got {row[1]}"
            assert str(row[2]) == str(expected['trace_lines']), \
                f"Row {i+1} trace_lines mismatch. Expected {expected['trace_lines']}, got {row[2]}"