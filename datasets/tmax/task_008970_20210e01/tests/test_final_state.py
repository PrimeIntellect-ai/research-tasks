# test_final_state.py

import os
import csv
import pytest

def test_data_copied():
    """Check if the jsonl files were copied to the data directory."""
    data_dir = "/home/user/workspace/data"
    expected_files = ["log_A.jsonl", "log_B.jsonl", "log_C.jsonl"]

    for f in expected_files:
        path = os.path.join(data_dir, f)
        assert os.path.isfile(path), f"Expected file {path} was not copied to the data directory."

def test_scripts_exist():
    """Check if the required scripts were created."""
    python_script = "/home/user/workspace/process_log.py"
    bash_script = "/home/user/workspace/run_pipeline.sh"

    assert os.path.isfile(python_script), f"Python script {python_script} is missing."
    assert os.path.isfile(bash_script), f"Bash script {bash_script} is missing."

def test_processed_files_exist():
    """Check if intermediate processed CSV files exist."""
    processed_dir = "/home/user/workspace/processed"
    expected_files = ["log_A.csv", "log_B.csv", "log_C.csv"]

    for f in expected_files:
        path = os.path.join(processed_dir, f)
        assert os.path.isfile(path), f"Processed intermediate file {path} is missing."

def test_final_series_csv():
    """Check if the final merged and interpolated CSV is correct."""
    final_csv = "/home/user/workspace/final_series.csv"
    assert os.path.isfile(final_csv), f"Final output file {final_csv} is missing."

    expected_data = [
        ("2023-11-01T00:00:00Z", 1000.0),
        ("2023-11-01T01:00:00Z", 1100.0),
        ("2023-11-01T02:00:00Z", 1200.0),
        ("2023-11-01T03:00:00Z", 1300.0),
        ("2023-11-01T04:00:00Z", 1400.0),
        ("2023-11-02T00:00:00Z", 2000.0),
        ("2023-11-02T01:00:00Z", 2250.0),
        ("2023-11-02T02:00:00Z", 2500.0),
        ("2023-11-03T10:00:00Z", 5000.0),
        ("2023-11-03T11:00:00Z", 5050.0),
        ("2023-11-03T12:00:00Z", 5100.0),
    ]

    actual_data = []
    with open(final_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["timestamp", "size_bytes"], f"Incorrect header in {final_csv}. Got {header}."

        for row in reader:
            assert len(row) == 2, f"Malformed row in {final_csv}: {row}"
            timestamp, size_bytes_str = row
            try:
                size_bytes = float(size_bytes_str)
            except ValueError:
                pytest.fail(f"Invalid size_bytes value '{size_bytes_str}' in row {row}")
            actual_data.append((timestamp, size_bytes))

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} rows, but got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual[0] == expected[0], f"Row {i+1}: Expected timestamp {expected[0]}, got {actual[0]}."
        assert abs(actual[1] - expected[1]) < 1e-5, f"Row {i+1}: Expected size_bytes {expected[1]}, got {actual[1]}."