# test_final_state.py

import os
import csv

def test_output_files_exist():
    """Verify that the required output files have been created."""
    assert os.path.isfile('/home/user/output/sampled_changes.csv'), "The output CSV file /home/user/output/sampled_changes.csv is missing."
    assert os.path.isfile('/home/user/output/pipeline.log'), "The output log file /home/user/output/pipeline.log is missing."

def test_csv_contents():
    """Verify the contents, formatting, and sorting of the sampled_changes.csv file."""
    csv_path = '/home/user/output/sampled_changes.csv'

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The CSV file is empty."

    expected_header = ['server', 'timestamp', 'config_val', 'cpu_load', 'high_load']
    assert rows[0] == expected_header, f"CSV header is incorrect. Expected {expected_header}, but got {rows[0]}."

    data_rows = rows[1:]
    assert len(data_rows) == 4, f"Expected exactly 4 data rows in the CSV, but found {len(data_rows)}."

    expected_data = [
        ['alpha', '2023-10-01T10:20:00Z', 'update1', '90.00', '1'],
        ['alpha', '2023-10-01T10:30:00Z', 'update2', '82.50', '1'],
        ['beta', '2023-10-01T10:05:00Z', 'start', '85.00', '1'],
        ['beta', '2023-10-01T10:15:00Z', 'error?', '85.00', '1']
    ]

    for i, (actual, expected) in enumerate(zip(data_rows, expected_data)):
        assert actual == expected, f"Data row {i+1} is incorrect.\nExpected: {expected}\nActual: {actual}"

def test_pipeline_log_contents():
    """Verify that the pipeline.log contains the exact expected metrics."""
    log_path = '/home/user/output/pipeline.log'

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in pipeline.log, but found {len(lines)}."

    expected_lines = [
        "Total lines read: 9",
        "Malformed lines fixed: 2",
        "Missing values imputed: 3"
    ]

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Log line {i+1} is incorrect.\nExpected: '{expected}'\nActual: '{actual}'"