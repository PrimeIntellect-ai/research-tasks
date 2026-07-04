# test_final_state.py

import os
import csv

def test_summary_csv_exists_and_correct():
    """Verify that summary.csv exists and contains the correct aggregated data."""
    summary_file = "/home/user/summary.csv"
    assert os.path.exists(summary_file), f"Output file {summary_file} does not exist."
    assert os.path.isfile(summary_file), f"Path {summary_file} is not a file."

    expected_data = [
        ["lang", "resource", "avg_value"],
        ["en", "cpu_ms", "125.00"],
        ["en", "mem_mb", "384.00"],
        ["en", "net_kb", "768.00"],
        ["es", "cpu_ms", "120.00"],
        ["es", "mem_mb", "512.00"],
        ["es", "net_kb", "1024.00"],
        ["fr", "cpu_ms", "200.00"],
        ["fr", "mem_mb", "1024.00"],
        ["fr", "net_kb", "2048.00"],
        ["zh", "cpu_ms", "250.00"],
        ["zh", "mem_mb", "1536.00"],
        ["zh", "net_kb", "3072.00"]
    ]

    actual_data = []
    with open(summary_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_data.append(row)

    assert len(actual_data) > 0, f"The file {summary_file} is empty."

    # Check header
    assert actual_data[0] == expected_data[0], f"Header row in {summary_file} is incorrect. Expected {expected_data[0]}, got {actual_data[0]}"

    # Check data rows
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} rows (including header), got {len(actual_data)}."

    for i in range(1, len(expected_data)):
        assert actual_data[i] == expected_data[i], f"Row {i} in {summary_file} is incorrect. Expected {expected_data[i]}, got {actual_data[i]}"