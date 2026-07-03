# test_final_state.py

import os
import pytest

def test_parquet_file_exists_and_valid():
    """Check if the cleaned_sensors.parquet file exists and has Parquet magic bytes."""
    parquet_path = '/home/user/cleaned_sensors.parquet'
    assert os.path.isfile(parquet_path), f"File {parquet_path} is missing."

    # Check Parquet magic bytes (PAR1 at beginning and end)
    with open(parquet_path, 'rb') as f:
        header = f.read(4)
        assert header == b'PAR1', f"File {parquet_path} does not have a valid Parquet header."

        f.seek(-4, os.SEEK_END)
        footer = f.read(4)
        assert footer == b'PAR1', f"File {parquet_path} does not have a valid Parquet footer."

def test_correlation_csv_exists_and_correct():
    """Check if the correlation.csv file exists and contains the exact expected matrix."""
    csv_path = '/home/user/correlation.csv'
    assert os.path.isfile(csv_path), f"File {csv_path} is missing."

    expected_lines = [
        "1.0000,0.4640,-0.5732",
        "0.4640,1.0000,-0.4072",
        "-0.5732,-0.4072,1.0000"
    ]

    with open(csv_path, 'r') as f:
        # Read lines, strip whitespace/newlines, filter out empty lines
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 rows in {csv_path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Row {i+1} mismatch. Expected '{expected}', got '{actual}'."