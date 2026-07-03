# test_final_state.py

import os
import re
import pytest

def test_raw_data_downloaded():
    """Test that raw data files were downloaded to /home/user/raw_data."""
    raw_dir = "/home/user/raw_data"
    assert os.path.isdir(raw_dir), f"Directory {raw_dir} is missing. Did you download the data?"

    expected_files = {"log1.json", "log2.json", "log3.json"}
    actual_files = set(os.listdir(raw_dir))

    missing = expected_files - actual_files
    assert not missing, f"Missing files in {raw_dir}: {missing}"

def test_etl_script_exists_and_uses_parallelism():
    """Test that the ETL script exists and uses multiprocessing or concurrent.futures."""
    script_path = "/home/user/etl.py"
    assert os.path.isfile(script_path), f"ETL script {script_path} is missing."

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    has_multiprocessing = "multiprocessing" in content
    has_concurrent = "concurrent.futures" in content

    assert has_multiprocessing or has_concurrent, (
        f"The script {script_path} must use 'multiprocessing' or 'concurrent.futures' "
        "to process the files in parallel."
    )

def test_hourly_max_csv():
    """Test that the output CSV exists and contains the correct aggregated data."""
    csv_path = "/home/user/hourly_max.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    expected_lines = [
        "2023-10-01T08:00:00Z,19.1",
        "2023-10-01T09:00:00Z,25.1",
        "2023-10-01T10:00:00Z,17.8",
        "2023-10-01T11:00:00Z,14.2"
    ]

    with open(csv_path, "r", encoding="utf-8") as f:
        # Read lines, strip whitespace/newlines, filter out empty lines
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {csv_path} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )