# test_final_state.py

import os
import csv
import pytest

def test_quarantine_file():
    quarantine_path = "/home/user/quarantine.jsonl"
    assert os.path.exists(quarantine_path), f"The file {quarantine_path} does not exist."
    assert os.path.isfile(quarantine_path), f"The path {quarantine_path} is not a regular file."

    with open(quarantine_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 1, f"Expected exactly 1 line in {quarantine_path}, found {len(lines)}."

    expected_line = '{"event_id": "6", "timestamp": "2023-10-01T10:00:00Z", "payload": "bad unicode \\u001Z", "response_time": 10.0}'
    assert lines[0].strip() == expected_line, f"The quarantined line does not match the expected malformed line."

def test_hourly_stats_file():
    stats_path = "/home/user/hourly_stats.csv"
    assert os.path.exists(stats_path), f"The file {stats_path} does not exist."
    assert os.path.isfile(stats_path), f"The path {stats_path} is not a regular file."

    with open(stats_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"The file {stats_path} is empty."

    expected_headers = ["hour", "event_count", "avg_response_time"]
    assert rows[0] == expected_headers, f"Expected headers {expected_headers}, but got {rows[0]}."

    expected_data = [
        ["2023-10-01T10:00:00Z", "2", "150.00"],
        ["2023-10-01T11:00:00Z", "2", "100.00"],
        ["2023-10-01T12:00:00Z", "1", "300.00"]
    ]

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} data rows, found {len(data_rows)}."

    for i, (actual, expected) in enumerate(zip(data_rows, expected_data)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}."