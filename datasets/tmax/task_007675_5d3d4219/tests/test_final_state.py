# test_final_state.py

import os
import pytest

ARCHIVE_PATH = "/home/user/archive/backup.tar.zst"
ID_SUM_PATH = "/home/user/id_sum.txt"
CLEANED_DATA_PATH = "/home/user/cleaned_data.csv"

def test_archive_exists():
    """Test that the raw data was compressed into the expected archive."""
    assert os.path.isfile(ARCHIVE_PATH), f"Archive not found at {ARCHIVE_PATH}"

def test_id_sum_correct():
    """Test that the exact precision-lossless sum of IDs is correct."""
    assert os.path.isfile(ID_SUM_PATH), f"ID sum file not found at {ID_SUM_PATH}"
    with open(ID_SUM_PATH, 'r') as f:
        actual_sum = f.read().strip()

    expected_sum = "9000000000000000500500"
    assert actual_sum == expected_sum, f"Sum mismatch: Expected {expected_sum}, got {actual_sum}"

def test_cleaned_data_exists():
    """Test that the cleaned data file exists."""
    assert os.path.isfile(CLEANED_DATA_PATH), f"Cleaned data not found at {CLEANED_DATA_PATH}"

def test_cleaned_data_columns():
    """Test that the correct columns were dropped (SensorB)."""
    with open(CLEANED_DATA_PATH, 'r') as f:
        header = f.readline().strip()

    expected_header = "ID,SensorA,SensorC"
    assert header == expected_header, f"Incorrect columns in cleaned data. Expected header '{expected_header}', got '{header}'"

def test_cleaned_data_imputation():
    """Test that NaNs were correctly imputed to 0.0 and no NaNs remain."""
    with open(CLEANED_DATA_PATH, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) == 1001, f"Expected 1001 lines in {CLEANED_DATA_PATH}, found {len(lines)}"

    for i, line in enumerate(lines):
        assert "NaN" not in line, f"Found 'NaN' in cleaned data at line {i + 1}: {line}"

    # Check row 10 (index 10) to ensure NaN was imputed to 0.0
    row_10 = lines[10].split(',')
    assert row_10[1] == "0.0", f"Expected '0.0' for SensorA at row 10, got {row_10[1]}"