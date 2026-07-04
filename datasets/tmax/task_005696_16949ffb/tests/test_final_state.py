# test_final_state.py

import os
import pytest

def test_processed_data_content():
    processed_data_path = "/home/user/processed_data.csv"
    assert os.path.exists(processed_data_path), f"File missing: {processed_data_path}"

    expected_rows = [
        "1599999940,1,25.0",
        "1599999940,2,25.5",
        "1600000000,1,25.4",
        "1600000240,1,24.0",
        "1600000240,2,24.1",
        "1600000000,2,26.1",
        "1600000060,1,25.5",
        "1600000120,2,26.3",
        "1600000180,1,25.8",
        "1600000180,2,26.5"
    ]

    with open(processed_data_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_rows, (
        f"Output mismatch in {processed_data_path}.\n"
        f"Expected {len(expected_rows)} rows: {expected_rows}\n"
        f"Actual {len(actual_lines)} rows: {actual_lines}"
    )

def test_etl_executable_exists():
    source_path = "/home/user/etl.c"
    executable_path = "/home/user/etl"

    assert os.path.exists(source_path), f"Source file {source_path} is missing."
    assert os.path.exists(executable_path), f"Executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."