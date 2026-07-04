# test_final_state.py

import os
import csv

def test_aggregated_csv_exists_and_correct():
    csv_path = "/home/user/loc_aggregated.csv"
    assert os.path.isfile(csv_path), f"Expected output CSV file {csv_path} does not exist."

    expected_rows = [
        ['hour', 'unique_events'],
        ['2023-10-01T10', '2'],
        ['2023-10-01T11', '2'],
        ['2023-10-02T08', '1']
    ]

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        actual_rows = [row for row in reader if row]

    assert actual_rows == expected_rows, f"CSV content does not match expected output. Got: {actual_rows}"

def test_pipeline_log_exists_and_correct():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Expected log file {log_path} does not exist."

    expected_logs = [
        "PIPELINE_START",
        "TOTAL_LINES: 8",
        "DUPLICATES_REMOVED: 3",
        "PIPELINE_COMPLETE"
    ]

    with open(log_path, 'r', encoding='utf-8') as f:
        actual_logs = [line.strip() for line in f if line.strip()]

    assert actual_logs == expected_logs, f"Log content does not match expected output. Got: {actual_logs}"