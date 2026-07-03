# test_final_state.py

import os
import csv
import pytest

def test_features_csv_exists():
    """Test that the output CSV file exists."""
    csv_path = "/home/user/features.csv"
    assert os.path.exists(csv_path), f"Output file is missing: {csv_path}"
    assert os.path.isfile(csv_path), f"Path exists but is not a file: {csv_path}"

def test_features_csv_content():
    """Test that the output CSV file has the correct content and formatting."""
    csv_path = "/home/user/features.csv"

    expected_rows = [
        ["seq1_short", "1.6094"],
        ["seq2_medium", "1.9080"],
        ["seq3_long", "1.6094"],
        ["seq4_mixed", "3.8797"]
    ]

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The CSV file is empty."

    header = rows[0]
    assert header == ["ID", "Entropy"], f"Expected header ['ID', 'Entropy'], but got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, but got {len(data_rows)}."

    for i, (actual, expected) in enumerate(zip(data_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."