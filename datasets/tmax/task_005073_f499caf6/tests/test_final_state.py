# test_final_state.py

import os
import pytest

def test_cpp_source_and_binary_exist():
    """Test that the C++ source file and compiled binary exist."""
    source_path = "/home/user/process.cpp"
    binary_path = "/home/user/process"

    assert os.path.exists(source_path), f"C++ source file {source_path} is missing."
    assert os.path.isfile(source_path), f"Path {source_path} is not a file."

    assert os.path.exists(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.path.isfile(binary_path), f"Path {binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_aggregated_csv_output():
    """Test that the aggregated.csv file exists and contains the correct aggregated data."""
    csv_path = "/home/user/aggregated.csv"
    assert os.path.exists(csv_path), f"Output CSV {csv_path} is missing."

    expected_csv = (
        "Hour,MeanValue,FailCount\n"
        "2023-10-12T08:00:00Z,46.1,1\n"
        "2023-10-12T09:00:00Z,42.0,2\n"
        "2023-10-13T10:00:00Z,10.0,0"
    )

    with open(csv_path, "r") as f:
        content = f.read().strip()

    assert content == expected_csv, f"The content of {csv_path} does not match the expected output.\nExpected:\n{expected_csv}\n\nGot:\n{content}"

def test_pipeline_log_output():
    """Test that the pipeline.log file exists and contains the correct log message."""
    log_path = "/home/user/pipeline.log"
    assert os.path.exists(log_path), f"Pipeline log {log_path} is missing."

    expected_log_line = "Processed 8 records. Found 3 unique hours."

    with open(log_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert any(expected_log_line in line for line in lines), f"Expected log line '{expected_log_line}' not found in {log_path}."