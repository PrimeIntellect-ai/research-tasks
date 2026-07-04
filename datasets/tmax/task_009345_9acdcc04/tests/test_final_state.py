# test_final_state.py

import os
import csv

def test_go_program_exists():
    """Test that the Go program was created at the expected location."""
    file_path = '/home/user/analyze_chains.go'
    assert os.path.isfile(file_path), f"The Go program {file_path} is missing."

def test_csv_output_exists():
    """Test that the output CSV file exists."""
    file_path = '/home/user/chain_summary.csv'
    assert os.path.isfile(file_path), f"The output CSV file {file_path} is missing."

def test_csv_output_content():
    """Test that the output CSV file contains the correct data and is sorted correctly."""
    file_path = '/home/user/chain_summary.csv'
    assert os.path.isfile(file_path), f"The output CSV file {file_path} is missing."

    expected_rows = [
        ['root_id', 'total_size_mb', 'chunk_count'],
        ['bkp_f2', '3500', '2'],
        ['bkp_f1', '1900', '4'],
        ['bkp_f3', '1150', '4']
    ]

    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) > 0, f"The CSV file {file_path} is empty."
    assert actual_rows[0] == expected_rows[0], f"Expected header {expected_rows[0]}, but got {actual_rows[0]}."

    # Check exact match for the rest of the rows to ensure correct values and sorting
    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows (including header), but got {len(actual_rows)}."

    for i in range(1, len(expected_rows)):
        assert actual_rows[i] == expected_rows[i], f"Row {i} mismatch. Expected {expected_rows[i]}, but got {actual_rows[i]}."