# test_final_state.py

import os
import csv
import pytest

CSV_PATH = '/home/user/paginated_tasks.csv'

def test_csv_exists():
    """Test that the output CSV file exists."""
    assert os.path.isfile(CSV_PATH), f"Output file not found at {CSV_PATH}"

def test_csv_contents():
    """Test that the CSV contains exactly the expected paginated results."""
    expected_rows = [
        ['E', '2', 'B'],
        ['J', '3', 'F'],
        ['I', '3', 'E'],
        ['H', '3', 'C'],
        ['G', '3', 'C']
    ]

    actual_rows = []
    with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # Skip empty lines if any
                actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."