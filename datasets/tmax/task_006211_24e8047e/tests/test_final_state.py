# test_final_state.py

import os
import csv
import pytest

def compute_expected_results():
    expected_sums = {}
    expected_counts = {}

    for i in range(1, 51):
        filepath = f'/home/user/telemetry_data/telemetry_{i:02d}.csv'
        if not os.path.exists(filepath):
            continue

        with open(filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            continue

        data_rows = rows[1:]

        # Remove exact duplicate rows within each file
        seen = set()
        unique_rows = []
        for row in data_rows:
            row_tuple = tuple(row)
            if row_tuple not in seen:
                seen.add(row_tuple)
                unique_rows.append(row)

        for row in unique_rows:
            if len(row) != 6:
                continue

            ts, srv, c1, m1, c2, m2 = row
            srv = srv.strip().upper()

            def is_missing(v):
                return v == "" or v == "NaN"

            if is_missing(c1) and is_missing(m1) and is_missing(c2) and is_missing(m2):
                continue

            def get_val(v):
                return 0.0 if is_missing(v) else float(v)

            metrics = [
                ('node1', 'cpu', get_val(c1)),
                ('node1', 'mem', get_val(m1)),
                ('node2', 'cpu', get_val(c2)),
                ('node2', 'mem', get_val(m2)),
            ]

            for node_id, metric, val in metrics:
                key = (srv, node_id, metric)
                expected_sums[key] = expected_sums.get(key, 0.0) + val
                expected_counts[key] = expected_counts.get(key, 0) + 1

    expected_results = []
    for key in expected_sums:
        avg = round(expected_sums[key] / expected_counts[key], 2)
        # Format avg to 2 decimal places as string to match CSV output
        expected_results.append((*key, f"{avg:.2f}"))

    expected_results.sort()
    return expected_results

def test_summary_file_exists():
    assert os.path.exists('/home/user/telemetry_summary.csv'), "The output file /home/user/telemetry_summary.csv does not exist."
    assert os.path.isfile('/home/user/telemetry_summary.csv'), "/home/user/telemetry_summary.csv is not a file."

def test_summary_file_content():
    filepath = '/home/user/telemetry_summary.csv'
    assert os.path.exists(filepath), "Output file missing."

    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The output file is empty."

    header = rows[0]
    expected_header = ['server_id', 'node_id', 'metric', 'average_value']
    assert header == expected_header, f"Incorrect header. Expected {expected_header}, but got {header}."

    actual_data = rows[1:]
    expected_data = compute_expected_results()

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} rows, but got {len(actual_data)} rows."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        # Convert the actual average to float then format to ensure matching
        try:
            actual_avg = f"{float(actual[3]):.2f}"
            actual_formatted = (actual[0], actual[1], actual[2], actual_avg)
        except ValueError:
            actual_formatted = tuple(actual)

        assert actual_formatted == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual_formatted}."