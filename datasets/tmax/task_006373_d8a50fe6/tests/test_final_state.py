# test_final_state.py

import os
import csv
import pytest

def test_schema_errors_log():
    log_path = '/home/user/schema_errors.log'
    assert os.path.exists(log_path), f"Expected log file {log_path} does not exist."
    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ids = {'2', '6'}
    assert set(lines) == expected_ids, f"Expected schema errors {expected_ids}, but got {set(lines)}"

def test_overflow_errors_log():
    log_path = '/home/user/overflow_errors.log'
    assert os.path.exists(log_path), f"Expected log file {log_path} does not exist."
    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ids = {'4', '8'}
    assert set(lines) == expected_ids, f"Expected overflow errors {expected_ids}, but got {set(lines)}"

def test_math_anomalies_log():
    log_path = '/home/user/math_anomalies.log'
    assert os.path.exists(log_path), f"Expected log file {log_path} does not exist."
    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ids = {'3'}
    assert set(lines) == expected_ids, f"Expected math anomalies {expected_ids}, but got {set(lines)}"

def test_valid_data_csv():
    csv_path = '/home/user/valid_data.csv'
    assert os.path.exists(csv_path), f"Expected output file {csv_path} does not exist."

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['id', 'x1', 'x2', 'model_output'], f"CSV header is incorrect: {header}"

        rows = list(reader)

    expected_ids = ['1', '5', '7', '9']
    actual_ids = [row[0] for row in rows if row]

    assert actual_ids == expected_ids, f"Expected valid data IDs {expected_ids} in order, but got {actual_ids}"

    # Check specific values for the first valid row to ensure data integrity
    assert rows[0] == ['1', '2.0', '3.0', '11.5'], f"First valid row data mismatch: {rows[0]}"