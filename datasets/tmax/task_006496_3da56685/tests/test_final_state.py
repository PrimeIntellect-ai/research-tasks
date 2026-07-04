# test_final_state.py

import os
import pytest

def test_parquet_file_exists_and_valid():
    """Test that the processed Parquet file exists and has valid Parquet magic bytes."""
    parquet_path = '/home/user/processed_data.parquet'

    assert os.path.exists(parquet_path), f"Missing processed file: {parquet_path}"
    assert os.path.isfile(parquet_path), f"Expected a file: {parquet_path}"
    assert os.path.getsize(parquet_path) > 0, f"File is empty: {parquet_path}"

    with open(parquet_path, 'rb') as f:
        data = f.read()

    assert data.startswith(b'PAR1'), "File does not start with Parquet magic bytes 'PAR1'."
    assert data.endswith(b'PAR1'), "File does not end with Parquet magic bytes 'PAR1'."

def test_parquet_columns_present():
    """Test that the required columns are present in the Parquet file metadata."""
    parquet_path = '/home/user/processed_data.parquet'

    with open(parquet_path, 'rb') as f:
        data = f.read()

    expected_columns = [b'id', b'timestamp', b'magnitude', b'temp_norm', b'pressure']

    for col in expected_columns:
        assert col in data, f"Column {col.decode()} not found in Parquet file metadata."

def test_summary_file_contents():
    """Test that the summary.txt file exists and contains the correct mean values."""
    summary_path = '/home/user/summary.txt'

    assert os.path.exists(summary_path), f"Missing summary file: {summary_path}"
    assert os.path.isfile(summary_path), f"Expected a file: {summary_path}"

    with open(summary_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    expected_content = "Mean Magnitude: 99.8291\nMean Temp Norm: 4.0264"

    # Normalize line endings
    content = content.replace('\r\n', '\n')

    assert content == expected_content, f"Summary file contents do not match expected values.\nExpected:\n{expected_content}\nGot:\n{content}"